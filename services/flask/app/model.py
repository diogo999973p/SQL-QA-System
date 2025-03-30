import os
from openai import OpenAI


DATABASE_DESCRIPTION = """
Forget everything you know about the bikeStores database and consider the following:

The sales.stores table represents the physical retail locations where bike products are sold. It contains the column store_id, which uniquely identifies each store, store_name to describe the store, phone and email for contact, and address-related columns: street, city, state, and zip_code, which provide the store’s location details.
The sales.staffs table holds information about store employees. The staff_id column serves as a unique identifier, while first_name and last_name store the employee’s name. The email and phone columns provide contact information. The active column indicates if the employee is currently working. The store_id column links the employee to a specific store, and the manager_id column references another staff member who acts as their manager.  
The sales.customers table contains details of people who purchase products. The customer_id column uniquely identifies each customer, while first_name and last_name store their name. The email and phone columns provide contact details. Address-related information is stored in street, city, state, and zip_code.  
The production.categories table categorizes products into different types. It includes the category_id column as a unique identifier and the category_name column to describe the type of product, such as "Mountain Bikes" or "Road Bikes."  
The production.brands table stores information about product manufacturers. The brand_id column uniquely identifies each brand, while the brand_name column contains the brand’s name.  
The production.products table maintains all items available for sale. The product_id column uniquely identifies each product, while product_name provides its name. The brand_id column links the product to a specific brand, and the category_id column associates it with a category. The model_year column indicates the year of the product model, and list_price stores its selling price.  
The production.stocks table tracks product availability in different stores. The store_id column identifies the store, the product_id column specifies the product, and the quantity column records how many units are available at that location.  
The sales.orders table records purchases made by customers. The order_id column serves as a unique identifier, while customer_id links the order to the customer who placed it. The order_status column indicates the order’s current state, and order_date records the date of purchase. The required_date and shipped_date columns track when the order was expected and when it was shipped. The store_id column identifies the store where the order was placed, and staff_id links the order to the employee who processed it.  
The sales.order_items table holds detailed information about products in each order. The order_id column associates the record with a specific order, and item_id uniquely identifies each item within that order. The product_id column links to the product being sold. The quantity column specifies the number of units purchased, while list_price records the price at the time of sale. The discount column stores any applied discount.  

Relationships:
The production.products table is related to production.categories through the category_id column, ensuring that each product belongs to a specific category. It is also linked to production.brands through the brand_id column, indicating the manufacturer of each product.  
The production.stocks table establishes a relationship between production.products and sales.stores by using the product_id and store_id columns, respectively, keeping track of inventory in different store locations.  
The sales.orders table connects with sales.customers via the customer_id column, allowing each order to be associated with the customer who placed it. It also relates to sales.stores through the store_id column, indicating where the purchase took place. Additionally, it links to sales.staffs through the staff_id column, identifying the employee responsible for handling the sale.  
The sales.order_items table is related to sales.orders via the order_id column, ensuring each order item belongs to a specific purchase. It is also linked to production.products through the product_id column, specifying the product included in the order.  
The sales.staffs table has a self-referential relationship using the manager_id column, meaning that each staff member can report to another staff member who is their manager. Furthermore, it connects to sales.stores via the store_id column, indicating where each employee works.
"""

FIRST_STEP_DESCRIPTION = """
You are an SQL Generator chatbot that only responds with SQL code in SQL SERVER dialect considering the above text.

Do not put any character or symbol that is not part of the SQL command. Put aliases while using SQL functions. 
If there is two or more SQL commands, separate them with semicolon.
"""


class Model:
    def __init__(self, model_name):
        self.model_name = model_name

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=f"{os.getenv('OPENROUTER_API_KEY')}",
        )


    def generate_text(self, first_instruction, second_instruction, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "developer",
                        "content": first_instruction
                    },
                    {
                        "role": "developer",
                        "content": second_instruction
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"An error occurred: {e}"
        


class ModelAnswerParser:
    def __init__(self):
        pass

    def get_queries_from_model_answer(self, answer):
        self.answer = answer

        cleaned_answer = answer.replace('sql', '').replace('`','')
        
        queries = [query.strip() for query in cleaned_answer.split(';') if query.strip()]

        return queries