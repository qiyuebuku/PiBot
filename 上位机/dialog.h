#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>

namespace Ui {
class Dialog;
}

class Dialog : public QDialog
{
    Q_OBJECT

public:
    explicit Dialog(QWidget *parent = 0);
    ~Dialog();
public slots:
    void flashPic();

private:
    Ui::Dialog *ui;
    QTcpSocket *socket;
};

#endif // DIALOG_H
