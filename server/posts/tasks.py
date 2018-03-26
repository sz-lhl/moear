import json
import logging
import stevedore
from collections import OrderedDict

from celery import shared_task
from posts.models import *
from posts.serializers import *
from spiders.models import *
from spiders.serializers import *

log = logging.getLogger(__name__)


@shared_task
def package_post(post_pk_list):
    '''
    将传入的 Post 列表打包成 Mobi 文件
    '''
    post_list = [Post.objects.get(pk=pk) for pk in post_pk_list]

    # 将文章列表以时间倒序排列
    post_list.sort(key=lambda post: post.date, reverse=True)

    package_group = OrderedDict()
    for post in post_list:
        postmeta_list = PostMeta.objects.filter(post=post)
        postmeta_data = PostMetaSerializer(postmeta_list, many=True).data
        post_data = PostSerializer(post).data
        post_data['meta'] = postmeta_data

        spider_name = post.spider.name

        spider_data = SpiderSerializer(post.spider).data
        spdiermeta_list = SpiderMeta.objects.filter(spider=post.spider)
        spidermeta_data = SpiderMetaSerializer(spdiermeta_list, many=True).data
        spider_data['meta'] = spidermeta_data

        package_module = spidermeta_data.get('package_module', '')

        package_group.setdefault(package_module, OrderedDict())
        package_group[package_module].setdefault(spider_name, OrderedDict())
        package_group[package_module][spider_name].setdefault(
            'spider', spider_data)
        package_group[package_module][spider_name].setdefault('data', [])
        package_group[package_module][spider_name]['data'].append(post_data)

    log.debug('根据Package&Spider分组并序列化后的数据字典: {}'.format(
        json.dumps(package_group, ensure_ascii=False)))

    for package_module, spider_group in package_group.items():
        for spider_name, package_group in spider_group.items():
            # 通过调用指定 Spider 驱动，对文章列表数据进行格式化
            spider_mgr = stevedore.driver.DriverManager(
                namespace='moear.spider',
                name=spider_name,
                invoke_on_load=True,
            )
            posts_data = spider_mgr.driver.format(
                package_group.get('data', []))
            log.debug('经过Spider格式化后的文章列表: {}'.format(
                json.dumps(posts_data, ensure_ascii=False)))

            # 通过调用指定 Package 驱动，获取最终打包返回的mobi文件数据
            package_mgr = stevedore.driver.DriverManager(
                namespace='moear.package',
                name=package_module,
                invoke_on_load=True,
                invoke_args=(package_group.get('spider', {}),)
            )
            mobi_file = package_mgr.driver.generate(posts_data)
            # TODO 从系统settings中获取mobi暂存路径，并将mobi_file保存成文件
