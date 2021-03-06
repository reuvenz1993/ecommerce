from ecommerce.models import *
from sqlalchemy import func, or_
from flask_login import login_user, current_user
from ecommerce.functions import save_photo
import random 


def authenticate_buyer_Oauth(profile):
    print(profile)
    buyer = Buyer.query.filter_by(email= profile['email']).first()
    if buyer:
        login_user(buyer)
        return buyer
    else:
        new_buyer = Buyer(username=profile['name'], email=profile['email'], password=str(random.randint(1, 100000)), name=profile['name'])
        db.session.add(new_buyer)
        db.session.commit()
        new_buyer = Buyer.query.filter_by(email= profile['email']).first()
        login_user(new_buyer)
        return new_buyer

def handle_forms(forms):
    if forms['login_form'].login.data and forms['login_form'].validate_on_submit():
        return check_login(forms['login_form'])
    if forms['signup_form'].signup.data and forms['signup_form'].validate_on_submit():
        return signup_buyer(forms['signup_form'])


def check_login(login_form):
    buyer_logging = Buyer.query.filter_by(username = login_form.username.data).first()
    if ( buyer_logging is not None and buyer_logging.check_password(login_form.password.data) ) :
        to_remember = login_form.remember.data
        login_user(buyer_logging, remember = to_remember)
        print ('login scss')
        return {'login_successful': 'Logged in successfully'}
    elif buyer_logging is not None:
        return {'login_error': {'password': 'Password is incorrect'}}
    else :
        return {'login_error': {'username': 'Username does not exist'}}


def signup_buyer(signup_form):
    kwargs = { 'email':signup_form.email.data ,
                'username' :signup_form.username.data ,
                'password':signup_form.password.data ,
                'name':signup_form.name.data ,
                'address':signup_form.address.data}

    signup_error = {}
    if Buyer.query.filter_by(username = kwargs['username']).first():
        signup_error['username'] = 'Username already exists, Please Choose an other username'
    if  Buyer.query.filter_by(email = kwargs['email']).first() :
        signup_error['email'] = 'Email address is already in use'

    if signup_error:
        return {'signup_error': signup_error}

    if signup_form.photo.data:
        kwargs['photo'] = save_photo(photo=signup_form.photo.data, _dir='buyer_photo' )


    new_buyer = Buyer(**kwargs )
    db.session.add(new_buyer)
    db.session.commit()
    if Buyer.query.filter_by(username = kwargs['username']).first:
        return {'signup_successful': 'Signup successful'}
    else:
        return {'signup_error': 'unknown reason'}
    



def update_buyer_message(item_id, buyer_message):
    cart = Cart.query.get(item_id)
    cart.add_buyer_message(buyer_message=buyer_message)
    return buyer_message == cart.buyer_message


def remove_from_cart(item_id):
    cart = Cart.query.get(item_id)
    cart.cancal()
    return Cart.query.get(item_id).status == 3


def buy_all(buyer_id=None, **kwargs):
    if buyer_id :
        buyer = Buyer.query.get(buyer_id)
    elif current_user :
        buyer = current_user
    else:
        return False

    for item in buyer.open_cart:
        buy_one(item_id=item.id)
    if len(buyer.open_cart) == 0 :
        return True
    else:
        return False

# buy one product from those in the cart, pram : *[1]-cart.id , [2]-buyer_message
def buy_one(item_id):
    cart_item = Cart.query.get(item_id)
    order_id = cart_item.stamp_ordered()
    return order_id


def buy_now(product_id ,qty ,buyer_id, buyer_message=False, **kwargs):
    
    params = {'product_id': product_id, 'buyer_id': buyer_id,
              'qty': int(qty),'buyer_message': buyer_message}

    cart = Cart(**params, buy_now=True)
    db.session.add(cart)
    db.session.commit()
    if Cart.query.get(cart.id):
        return { 'cart_item':cart.id, 'cart_size': Buyer.query.get(buyer_id).open_cart_count, 'order_id': cart.order_id.id, 'product_name': cart.cart_product.name }
    else :
        return False

def add_to_cart(product_id ,qty ,buyer_id, **kwargs):

    cart = Cart(buyer_id=buyer_id, product_id=product_id, qty=int(qty), buy_now=False)
    db.session.add(cart)
    db.session.commit()
    if Cart.query.get(cart.id):
        return { 'cart_item':cart.id, 'cart_size': Buyer.query.get(buyer_id).open_cart_count }
    else :
        return False


def get_product_extra_info(pid):
    product = Product.query.filter_by(id = pid).first()
    if not product :
        print('product number : ' + str(pid) + ' not exists')
        return False

    product_data = product.__dict__
    product_data['supplier'] = product.supplier.get_info()
    product_data['reviews'] = product.get_review(get_review=True ,avg=True , count=True)
    reviews = []
    for rev in product_data['reviews']['get_review']:
        temp = rev
        rev = temp.__dict__
        rev['reviewer'] = temp.get_review_buyer().name
        if rev['_sa_instance_state']:
            del rev['_sa_instance_state']
        reviews.append(rev)
    product_data['reviews']['get_review'] = reviews
    product_data['orders'] = product.get_product_orders( get_product_orders=False, count_orders=True , count_units=True)
    product_data['price'] = round( float( product_data['price'] ) , 1 )
    if product_data['_sa_instance_state']:
        del product_data['_sa_instance_state']

    return product_data


def search( pid = [i for i in range( Product.query.count()+1 )] , category_list = [i for i in range( Category.query.count()+1 )] ,min_price=0 , max_price=100000 , min_avg=0 , word=False , as_json=False ):
    
    if type(pid) == int :
        pid = [pid]

    if type(category_list) == int :
        category_list = [category_list]

    if type(min_price) != int :
        min_price = int(min_price[0])

    if type(max_price) != int :
        max_price = int(max_price[0])

    if type(min_avg) != int :
        max_price = int(min_avg[0])


    search_query = db.session.query(Product.id).outerjoin(Order).outerjoin(Reviews).group_by(Product).having(or_(db.func.count(Reviews.id)==0 , db.func.avg(Reviews.stars) > min_avg )).subquery()


    if word :
        word = "%{}%".format(word)
        search_query = Product.query.join(search_query , search_query.c.id == Product.id).filter(Product.name.like(word)).subquery()

    
    search_query = Product.query.join(search_query , search_query.c.id == Product.id).filter(Product.id.in_(pid) , Product.category.in_(category_list) , Product.price > min_price , Product.price < max_price )

    if as_json:
        products = []
        for product in search_query :
            row = product.__dict__
            row['supplier'] = product.supplier.get_info()
            row['reviews'] = product.get_review(get_review=False ,avg=True , count=True)
            row['orders'] = product.get_product_orders( get_product_orders=False, count_orders=True , count_units=True)
            row['price'] = round( float( row['price'] ) , 1 )
            if row['_sa_instance_state']:
                del row['_sa_instance_state']
            products.append(row)
        return products
    else :
        return search_query





"""
def buy_now_or_add_to_cart(buyer_id , product_id , qty , buyer_message=False , buy_now=False ):
    if not Buyer.query.get(buyer_id) or not Product.query.get(product_id):
        return False

    kwargs = { 'buyer_id' : buyer_id ,
               'product_id' : product_id,
               'qty' : qty ,
               'buy_now' : buy_now ,
               'buyer_message': buyer_message}
    # if buyer choose buy now on product screen, prama
    if buy_now :
        if buyer_message :
            kwargs['buyer_message'] = buyer_message
        cart_item = Cart(**kwargs)
        if cart_item.order_id:
            return cart_item.order_id.id
        else :
            return False
    # if buyer choose "add to cart, on kwargs buyer_message=False so item will only be added to cart "
    else :
        cart_item = Cart( **kwargs )
        db.session.add(cart_item)
        db.session.commit()
        if Cart.query.get(cart_item.id):
            return { 'cart_item':cart_item.id , 'cart_size': Buyer.query.get(buyer_id).cart.filter(Cart.status == 1).count() }
        else :
            return False
"""



'''
def category_list(short=False):
    if short:
        return get_dict(Category.query.all())
    data = db.session.query(Category.id , Category.name , db.func.count(Product.id)).outerjoin(Product).group_by(Category).all()
    return data
'''

'''
def pull_buyer_orders(buyer_id):
    order_list = []
    for order in Buyer.query.get(buyer_id).orders:
        temp = order.__dict__
        temp['supplier_name'] = order.get_order_supplier().name
        temp['unit_price'] = int(temp['unit_price'])
        temp['total_price'] = float(temp['unit_price'])
        temp['order_time'] = str(temp['order_time'])[0:16]
        temp['product'] = get_product_extra_info(temp['product_id'])
        if '_sa_instance_state' in temp:
            del temp['_sa_instance_state']

        order_list.append(temp)

    return order_list
'''



'''
def pull_cart(buyer_id):
    cart = []
    total = 0
    for item in Buyer.query.get(buyer_id).get_cart():
        cart_item = item.__dict__
        if cart_item['_sa_instance_state']:
            del cart_item['_sa_instance_state']
        cart_item['unit_price'] = float( Product.query.get(item.product_id).price )
        cart_item['total'] = cart_item['unit_price'] * int(item.qty)
        total += cart_item['total']
        cart_item['product']=get_product_extra_info(cart_item['product_id'])
        cart.append(cart_item)
    
    return { 'cart' : cart , 'cart_size': len(cart) , 'total_cart_price' : total }
'''

'''
@app.route('/get_results', methods = ['GET', 'POST'])
def get_results():
    product_type = request.form['product_type'].lower()
    min_price = request.form['min_price']
    max_price = request.form['max_price']
    min_stars = request.form['min_stars']
    products = get_relvent_results(product_type , min_price , max_price , min_stars)
    return jsonify( products )
'''

'''
def get_reviews(pid):
    orders = Order.query.filter_by(product_id = pid).all()
    order_list = []
    reviews = []
    for order in orders:
        order_list.append( order.as_list() )
        reviews.append(order.as_list()[9][0].as_list())
    for review in reviews:
        review_order = Order.query.filter_by(id = review[1]).one()
        buyer = Buyer.query.filter_by(id = review_order.buyer_id).one()
        review.append(buyer.name)
    return reviews
'''

'''
def get_products(filters):
    products = Product.query
    
    for key , value in filters.items():
        if value is not None :
            temp = str(key+" == '"+value+"'")
            temp2 = str(key+" == "+value)
            temp3 = str(key+" == '"+value+"'")
            products = products.filter(temp)

    print('gfhfgh')
    products = products.all()
    return products
'''

'''
def get_relvent_results(product_type , min_price = 0 , max_price = 100000 , min_stars = 1):
    if product_type != 'all':
        temp = str(product_type)
        products = Product.query.filter(Product.product_type == temp)
    else:
        products = Product.query

    products = products.filter(Product.price > min_price , Product.price < max_price )
    products = products.all()
    product_list = []
    for p in products:
        product_list.append( p.as_list() )
    for prod in product_list:
        prod.append(get_product_extra_info(prod[0]))
    return product_list
'''


'''
def product_supplier_name(pid):
    product = Product.query.filter_by(id = pid).first()
    supplier = Supplier.query.filter_by(id = product.supplier_id).first()
    return supplier.name
'''
