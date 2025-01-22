# from django.test import TestCase, Client
# from django.contrib.auth import get_user_model
# from general.serializers import UserSerializer
# from django.contrib.auth.models import  Group
# from django.urls import reverse
# from django.core.files.uploadedfile import SimpleUploadedFile
# from moto import mock_s3
# from config.settings.local import AWS_STORAGE_BUCKET_NAME
# from rest_framework import status
# import boto3, io

# client = Client()
# User = get_user_model()

# class UserTests(TestCase):
#     def setUp(self):
#         user = User.objects.get_or_create(username='admin')[0]
#         client.force_login(user)
#         self.IMAGE_MAX = 5
#         self.fake_image_BytesIO =  b"fake_image_content"
#         self.user1 = User.objects.create(username="admin_user", password="cambiame", is_superuser=True, first_name="Izacar", last_name="Muños", email="izacar@mail.com", is_staff=True, is_active=True, date_joined="2018-11-02T15:07:02.653Z", last_login= None )
#         self.fake_image = SimpleUploadedFile("fake_image.png", self.fake_image_BytesIO, content_type="image/*")
#         self.fake_image_list = [SimpleUploadedFile(f"fake_image_{i}.png", self.fake_image_BytesIO, content_type="image/*") for i in range(self.IMAGE_MAX)]
     

#     def test_user_info(self):
#         response = client.get(reverse('get_user_info_by_name', kwargs={'username': 'admin_user'}))
#         user_serial = User.objects.get(username=self.user1.username)
#         serial = UserSerializer(user_serial)

#         self.assertEqual(str(response.data.get('id')), str(serial.data.get('id')))
#         self.assertEqual(str(response.data.get('username')), str(serial.data.get('username')))
#         self.assertEqual(str(response.data.get('email')), str(serial.data.get('email')))
#         self.assertEqual(str(response.data.get('is_active')), str(serial.data.get('is_active')))

#     @mock_s3
#     def test_upload_profile_picture(self):
#         conn = boto3.resource('s3')
#         conn.create_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
        
#         test_data = {'image': self.fake_image, 'user':self.user1.id}
#         response = client.post(reverse('post_get_all_profile_picture', kwargs={'user_id':str(self.user1.id)}), data=test_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


#     @mock_s3
#     def test_data_response_upload_profile_picture(self):
#         conn = boto3.resource('s3')
#         conn.create_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)

#         test_data = {'image': self.fake_image, 'user':self.user1.id}
#         response = client.post(reverse('post_get_all_profile_picture', kwargs={'user_id':str(self.user1.id)}), data=test_data)

#         data_response = response.data
#         profile_picture_id = data_response.get('id', 0)
#         get_image_url = f'/api/v1/user/{self.user1.id}/profile_picture/{profile_picture_id}'

#         self.assertEqual(data_response.get('user'), self.user1.id)
#         self.assertEqual(data_response.get('current'), True)
#         self.assertEqual(data_response.get('name'), self.fake_image.name)
#         self.assertEqual(get_image_url, data_response.get('image'))
#         self.assertIn('version', data_response)
    

#     @mock_s3
#     def test_get_all_profile_picture(self):
#         conn = boto3.resource('s3')
#         conn.create_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
#         profile_picture_list = []

#         for image in self.fake_image_list:
#             test_data = {'image': image, 'user':self.user1.id}
#             response = client.post(reverse('post_get_all_profile_picture', kwargs={'user_id':str(self.user1.id)}), data=test_data)
#             data_response = response.data
#             profile_picture_list.append(data_response)
            
        
#         get_all_response =  client.get(reverse('post_get_all_profile_picture', kwargs={'user_id':str(self.user1.id)}))
#         get_all_data_response = sorted(get_all_response.data, key = lambda profile_picture: profile_picture['id']) 
#         self.assertEqual(len(profile_picture_list), len(get_all_data_response))
#         for profile_picture, get_profile_picture in zip(profile_picture_list, get_all_data_response):

#             self.assertEqual(profile_picture.get('id'), get_profile_picture.get('id'))
#             self.assertEqual(profile_picture.get('name'), get_profile_picture.get('name'))
#             self.assertEqual(profile_picture.get('image'), get_profile_picture.get('image'))
    
#     @mock_s3
#     def test_set_current_profile_picture(self):
#         conn = boto3.resource('s3')
#         conn.create_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
#         profile_picture_list = []
#         current_profile_picture = {}

#         for image in self.fake_image_list:
#             test_data = {'image': image, 'user':self.user1.id}
#             response = client.post(reverse('post_get_all_profile_picture', kwargs={'user_id':str(self.user1.id)}), data=test_data)  ## new profile picture
#             current_profile_picture = response.data 
            
#         filter_function = lambda x: (x.get('current') == True)
#         get_all_response =  client.get(reverse('post_get_all_profile_picture', kwargs={'user_id':str(self.user1.id)}))
#         get_current_profile_picture_list = list(filter(filter_function, get_all_response.data))
#         get_current_profile_picture = get_current_profile_picture_list[0]

#         self.assertEqual(len(get_current_profile_picture_list), 1)
#         self.assertEqual(current_profile_picture.get('id'), get_current_profile_picture.get('id'))
#         self.assertEqual(current_profile_picture.get('name'), get_current_profile_picture.get('name'))
#         self.assertEqual(current_profile_picture.get('image'), get_current_profile_picture.get('image'))
#         self.assertEqual(current_profile_picture.get('current'), get_current_profile_picture.get('current'))
    

#     @mock_s3
#     def test_download_current_profile_picture(self):
#         conn = boto3.resource('s3')
#         conn.create_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
  
#         test_data = {'image': self.fake_image, 'user':self.user1.id}
#         response = client.post(reverse('post_get_all_profile_picture', kwargs={'user_id':str(self.user1.id)}), data=test_data)  ## new profile picture
#         image_id = response.data.get('id', 0)


#         response =  client.get(reverse('get_profile_picture_version', kwargs={'user_id':str(self.user1.id),  'image_id': image_id}))
#         downloaded_file =  b''.join(response.streaming_content)

#         self.assertEqual(response.get('Content-Disposition'),f'attachment; filename="{self.fake_image.name}"')
#         self.assertEqual(downloaded_file, self.fake_image_BytesIO)

        
        

       



