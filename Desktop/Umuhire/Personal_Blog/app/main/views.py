from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Blog,Comment,Subscription
from .. import db,photos
from .forms import UpdateProfile,BlogForm,CommentForm,SubscribeForm,UpdateBlogForm
from flask_login import login_required,current_user
import datetime
from ..request import get_quote


@main.route('/')
def index():
    title = 'Personal blog'
    blogs = Blog.query.all()
    quote = get_quote()
    comments = Comment.query.all()
    return render_template('index.html',title = title,quote=quote, blogs=blogs)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    blog_count = Blog.count_blogs(uname)

    if user is None:
        abort(404)

    return render_template('profile/profile.html',user = user, blogs = blog_count)


@main.route('/user/<uname>/update', methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname = user.username))

    return render_template('profile/update.html', form = form)


@main.route('/user/<uname>/update/pic', methods = ['POST'])
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    return redirect(url_for('main.profile', uname = uname))


@main.route('/blog/new', methods = ['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        blog = form.text.data
       

        new_blog = Blog(blog_title = title,blog_content = blog,user = current_user)
        new_blog.save_blog()
        return redirect(url_for('main.index'))

    title = 'New Blog'
    return render_template('new_blog.html', title = title, blog_form = form)


@main.route('/blog/<int:id>', methods = ["GET","POST"])
def blog(id):
    blog = Blog.get_blog(id)
    posted_date = blog.posted.strftime('%b %d, %Y')
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.text.data

        new_comment = Comment(comment = comment, user = current_user, blog_id = blog)

        new_comment.save_comment()

    comments = Comment.get_comments(blog)

    return render_template('blog.html', blog = blog, comment_form = form,comments = comments, date = posted_date)



@main.route('/edit/blog/<int:id>',methods= ['GET','POST'])
@login_required
def update_blog(id):
   blog=Blog.query.filter_by(id=id).first()
   if blog is None:
        abort(404)

   form=UpdateBlogForm()
   if form.validate_on_submit():
         blog.title=form.title.data
         blog.content=form.content.data

         db.session.add(blog)
         db.session.commit()

         return redirect(url_for('main.index'))
   return render_template('update_blog.html',form=form)

@main.route('/subscribe/', methods=['GET', 'POST'])

def subscribe():
    """
    Function that enables one to subscribe to the blog
    """
    form = SubscribeForm()
    if form.validate_on_submit():
        subscription = Subscription(email=form.email.data)
        db.session.add(subscription)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('subscribes.html', form=form)

@main.route('/delete_blog/<int:id>', methods = ["GET","POST"])
@login_required
def delete_blog(id):
    blog = Blog.get_blog(id)
    
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('.index'))

