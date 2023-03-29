from django.db import models
import string
from django.utils.text import slugify
import random
from django.urls import reverse
from PIL import Image
# Create your models here.
from django.contrib.auth.models import User

def upload_to_media():
    path = 'media/'
    return path

def random_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for str_ in range(8))

class Post(models.Model):
    STATUS = (
                (0,"Draft"),
                (1,"Publish")
                    )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    #added this cover to have images in the blog
    cover = models.ImageField(upload_to= upload_to_media())

    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + '-'+ random_slug())
        super().save()
        img = Image.open(self.cover.path)
        if img.height>300 or img.width>300:
            imageparam = (300,300)
            img.thumbnail(imageparam)
            img.save(self.cover.path)
        super(Post, self).save(*args,**kwargs)

    #auto redirect to post detail after publishing
    def get_absolute_url(self):
        return reverse ('post_detail', kwargs = {'slug':self.slug})

    @property
    def display_content(self):
        if len(self.content)>200:
            return f'{self.content[:200]} ... '
        return self.content
        
