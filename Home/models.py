from django.db import models

class Contact(models.Model):
	sno = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	phone = models.CharField(max_length=13)
	content = models.TextField()
	timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return 'Message from ' +self.name + ' - ' +self.email
	


class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.CharField(max_length=50)
    slug = models.CharField(max_length=130)
    timeStamp = models.DateTimeField(blank=True)


    def __str__(self):
        return self.title + ' by ' + self.author
    
