#include "test3.h"

test3::test3(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
	socket = new QTcpSocket;
	socket->connectToHost("192.168.1.1",2001);
	QTimer *mytimer = new QTimer;
	mytimer->start(800);
	connect(mytimer,SIGNAL(timeout()),this,SLOT(flashPic()));
}

test3::~test3()
{

}
void test3::flashPic()
{
	qDebug("flash!");
	ui.webView->setUrl(QUrl("http://192.168.1.1:8080/?action=snapshot"));
	ui.webView->update();
}
