#include "dialog.h"
#include "ui_dialog.h"

Dialog::Dialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Dialog)
{
    ui->setupUi(this);
    ui.setupUi(this);
    socket = new QTcpSocket;
    socket->connectToHost("192.168.1.1",2001);
    QTimer *mytimer = new QTimer;
    mytimer->start(800);
    connect(mytimer,SIGNAL(timeout()),this,SLOT(flashPic()));
}

Dialog::~Dialog()
{
    delete ui;
}

void Dialog::flashPic()
{
        qDebug("flash!");
        ui.webView->setUrl(QUrl("http://192.168.1.1:8080/?action=snapshot"));
        ui.webView->update();
}
