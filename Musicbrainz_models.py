from django.db import models


class musicbrainz_tag(models.Model):
    id =models.IntegerField(primary_key=True)
    gid = models.UUIDField()
    name = models.CharField(max_length=50)

class musicbrainz_artist(models.Model):
    id =models.IntegerField(primary_key=True)
    gid = models.UUIDField()
    name = models.CharField('艺术家',max_length=200)
    tag = models.ManyToManyField(musicbrainz_tag,related_name='artists')

   
class musicbrainz_release(models.Model):
    id =models.IntegerField(primary_key=True)
    gid = models.UUIDField()
    name = models.CharField('专辑名称',max_length=200)
    artist_credit =models.IntegerField(default=0)
    artist = models.ManyToManyField(musicbrainz_artist,related_name='releases')
    publishdate = models.SmallIntegerField('发行年份',default=0)
    tag = models.ManyToManyField(musicbrainz_tag,related_name='releases')


class musicbrainz_recording(models.Model):
    id =models.IntegerField(primary_key=True)
    gid = models.UUIDField()
    name = models.CharField('歌曲名称',max_length=200)
    release = models.ForeignKey(musicbrainz_release,on_delete=models.CASCADE)
    artist = models.ManyToManyField(musicbrainz_artist,related_name='recordings')
    tag = models.ManyToManyField(musicbrainz_tag,related_name='recordings')



