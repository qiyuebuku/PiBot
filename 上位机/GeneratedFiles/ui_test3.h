/********************************************************************************
** Form generated from reading UI file 'test3.ui'
**
** Created by: Qt User Interface Compiler version 5.5.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_TEST3_H
#define UI_TEST3_H

#include <QtCore/QVariant>
#include <QtWebKitWidgets/QWebView>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_test3Class
{
public:
    QWidget *centralWidget;
    QVBoxLayout *verticalLayout;
    QWebView *webView;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *test3Class)
    {
        if (test3Class->objectName().isEmpty())
            test3Class->setObjectName(QStringLiteral("test3Class"));
        test3Class->resize(600, 400);
        centralWidget = new QWidget(test3Class);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        verticalLayout = new QVBoxLayout(centralWidget);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        webView = new QWebView(centralWidget);
        webView->setObjectName(QStringLiteral("webView"));
        webView->setUrl(QUrl(QStringLiteral("about:blank")));

        verticalLayout->addWidget(webView);

        test3Class->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(test3Class);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 600, 26));
        test3Class->setMenuBar(menuBar);
        mainToolBar = new QToolBar(test3Class);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        test3Class->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(test3Class);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        test3Class->setStatusBar(statusBar);

        retranslateUi(test3Class);

        QMetaObject::connectSlotsByName(test3Class);
    } // setupUi

    void retranslateUi(QMainWindow *test3Class)
    {
        test3Class->setWindowTitle(QApplication::translate("test3Class", "test3", 0));
    } // retranslateUi

};

namespace Ui {
    class test3Class: public Ui_test3Class {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_TEST3_H
