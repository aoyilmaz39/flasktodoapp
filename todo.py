from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:////Users/ahmet/OneDrive/Masaüstü/TodoApp/todo.db"
db=SQLAlchemy(app)#Bilgisayarımızda oluşturduğumuz database in yolunu veririz.
#
#
@app.route("/delete/<string:id>")
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/")
def index():
    todos=Todo.query.all()#Bu bize veri tabanımızdan bir liste dönücek ve bu listenin içinde bizim elemanlarımızın her birinin özelliği bize sözlük yapısı şeklinde gelicek
    return render_template("index.html",todos=todos)#Bu verilerimizi index.html e göndeririz

@app.route("/complete/<string:id>")#string id şeklinde dinamik url mizi yazarız
def completeTodo(id):
    todo=Todo.query.filter_by(id=id).first()#Todo sınıfından id si tıkladığımız id değeri olan elemanımızı aldık ve todo değişkenine atatık
    """
    if todo.complete== True:
        todo.complete=False
    else:
        todo.complete=True
    """
    todo.complete = not todo.complete# üstteki kod ile aynı işlevi görmektedir.
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add",methods=["POST"])
def addTodo():
    #burada name parametresine göre ekrana girilen dğerimizi alıcaz ve Todo classından bir obje oluşturarak ORM yapısını kullanarak veritabanımıza ekleme yapıcaz
    title=request.form.get("title")#böylece html sayfamızdaki title değerini form nesnesi aracılığıyla çekmiş oluyoruz
    newTodo=Todo(title=title,complete=False)#Tablomuzun özelliklerini giririz
    db.session.add(newTodo)#Bununla veri tabanına yeni nesnemizi ekleriz
    db.session.commit()#Veri tabanında değişiklik olduğu için burada commit yapmamız gerekir.

    return redirect(url_for("index"))

#
#
class Todo(db.Model): #classımızı ORM nin içindeki .Model yapısından gerçekleştiriyoruz.
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80))
    complete=db.Column(db.Boolean)#işimizi tamamlamışsak bunu True yapıcaz Tamamlamamışsak False yapıcaz bu alanın sadece 2 değer almasını istiyoruz.

if __name__=="__main__":
    db.create_all()#Bununla uygulama her çalıştığında app.run çalışıcak ancak db.create all her seferinde çalışmıyacak
    #o yüzden bunu buraya yazabiliriz
    app.run(debug=True)