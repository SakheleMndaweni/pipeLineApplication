from django.test import TestCase, Client
from .models import *
from django.contrib.auth.models import User, auth

from selenium import webdriver
# Product test
class ProductTest(TestCase):

    def create_product(self, name="only a test", description="yes, this is only a test"):
        return Product.objects.create(name=name, description=description)

    def test_Product_creation(self):
        w = self.create_product()
        self.assertTrue(isinstance(w, Product))

    def setUp(self):
        self.driver = webdriver.Firefox()
  
    def createUser(self,name,password):
        user = User.objects.create_user(username = name, password= password)
        user.save()
        new_profile = OrderClient.objects.create(user=user)
        new_profile.save()

        return new_profile

    def login_app(self):
        tempUser = self.createUser()
        self.driver.get("http://localhost:8000/")
        self.driver.find_element_by_id('id_title').send_keys(tempUser.user.username)
        self.driver.find_element_by_id('id_body').send_keys(tempUser.user.password)
        self.driver.find_element_by_id('submit').click()

        self.assertIn("http://localhost:8000/", self.driver.current_url)
    
    #test item item 
    def test_add_Item(self):
        tempUser = self.createUser('sakhele','1112334L')
        order  = Order.objects.create(orderClient =tempUser)
        order.save()
        product = self.create_product()
        #call the api to add
        c = Client()
        response = c.get("/order/", {'itemId':1, 'action':'add'})
        print(response.status_code)
        
        self.assertTrue(order.getNumberOfitems < 1)
  
    def tearDown(self):
        self.driver.quit

if __name__ == '__main__':
    unittest.main()