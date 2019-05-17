#ifndef TEST3_H
#define TEST3_H

#include <QtWidgets/QMainWindow>
#include "ui_test3.h"
#include <QTimer>

class test3 : public QMainWindow
{
	Q_OBJECT

public:
	test3(QWidget *parent = 0);
	~test3();
public slots:
	void flashPic();

private:
	Ui::test3Class ui;
	QTcpSocket *socket;
};

#endif // TEST3_H
