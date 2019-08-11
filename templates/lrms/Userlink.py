@receiver(post_save, sender=User)
def create_user_profile(self, sender, instance, created, **kwargs):
    if created:
        OwnerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(self, sender, instance, **kwargs):
    instance.ownerprofile.save()

#################
class OwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER, default='')
    nrc = models.CharField(max_length=20, blank=False, null=False)
    telephone = models.CharField(max_length=15, default='', null=True, blank=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(verbose_name='Date of Birth', default=datetime.date(1995, 04, 13))
    next_of_kin = models.CharField(max_length=50, blank=False, null=False)
    kin_relation = models.CharField(max_length=50, blank=False, null=False, verbose_name='Relationship Of Next'
                                                                                         'Of Kin')

    @property
    def age(self):
        age = int((datetime.datetime.now().date() - self.date_of_birth).days / 365.25)
        return age

    def get_absolute_url(self):
        return reverse('owner-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        owner_id = (str(self.user.first_name) + ' ' + str(self.user.last_name))
        return owner_id

--------------------------------------------------------
<form class="form-inline mt-2 mt-md-0">
          <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>