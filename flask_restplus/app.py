from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from db import connection, execute_query, execute_read_query
app = Flask(__name__)

import os
import json

# init app 
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Product Management API',
    description='A Product Management API',
)


basedir = os.path.abspath(os.path.dirname(__file__))


productRoutes = api.namespace('product-management/api', description='Product operations')


class ProductModel:
  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty


product = api.model('Product', {
    'id': fields.Integer(readonly=True, description='The Product unique identifier'),
    'name': fields.String(required=True, description='The name of the product'),
    'description': fields.String(required=True, description='The description of the product'),
    'price': fields.Float(required=True, description='The price of the product'),
    'qty': fields.Integer(required=True, description='the quantity of the product'),
})



@productRoutes.route('/products')
class ProductsList(Resource):
	def get(self):
		''' Get All Products'''
		all_products_query = "SELECT * from products"
		products = execute_read_query(all_products_query)
		productsList = []
		for product in products:
			print(products)
			productsList.append(vars(ProductModel(product[1],product[2],product[3],product[4])))
		return productsList, 200


@productRoutes.route('/product/<int:id>')
class Products(Resource):
	def get(self,id):
		''' Get a single product based on ID'''
		specific_product = "SELECT * from products WHERE id={}".format(id)
		products = execute_read_query(specific_product)
		_prodID = id - 1
		productsList = []
		for product in products:
			print(products)
			productsList.append(vars(ProductModel(product[1],product[2],product[3],product[4])))

		if (id < 1):
			return 'Input a correct product ID', 400
		elif (id > len(productsList)):
			return 'No product has a product ID number of %s' % id, 404
		else:
			return productsList[_prodID], 200

		# if (id < 1):
		# 	return 'Input a correct product ID', 400
		# elif (product == []):
		# 	return 'No product has a product ID number of %s' % id, 404
		# else:
		# 	return product, 200


		
	def delete(self,id):
		''' Delete a single product based on ID'''
		delete_product = "DELETE FROM products WHERE id=%s" % id
		products = execute_query(delete_product)
		
		if len(product) == 0:
			return 'no product present', 404
		else:
			return 'Product with product number %s is deleted' %id, 200

	@productRoutes.expect(product)
	def put(self,id):
		''' Update a single product based on ID'''
		product_update = "SELECT * from products WHERE id = %s" % id
		product_To_update = execute_read_query(product_update)

		if len(product_To_update) == 0:
			return 'no product present', 404
		else: 
			_payload = api.payload
			product_To_update = _payload

			_name = product_To_update['name']
			_description = product_To_update['description']
			_price = product_To_update['price']
			_qty = product_To_update['qty']
			
			update_exec_query = "UPDATE products SET name = '{}', description = '{}', price = {}, qty = {} WHERE id = {}".format(_name, _description,_price,_qty, id)

			fin = execute_read_query(update_exec_query)

			return 'updated', 200


# Run Server
if __name__ == '__main__':
	app.run(debug=True)