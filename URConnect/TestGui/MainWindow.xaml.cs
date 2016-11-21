using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using UniversalRobotsConnect;


namespace TestGui
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private RobotConnector _robotConnector;
        private RobotModel _myRobotModel;
        //private RobotController _robotController;

        public MainWindow()
        {
            InitializeComponent();
            //_robotConnector = new RobotConnector("172.16.74.129");
            _robotConnector = new RobotConnector("192.168.0.3", true);
            _myRobotModel = _robotConnector.RobotModel;
            
            _robotConnector.DashboardClient.PowerOff();

            //_robotConnector.DashboardClient.PowerOn();


            //_robotConnector.RTDE.SetConfigurableDigitalOutput(0, true);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(1, true);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(2, true);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(3, true);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(4, true);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(5, true);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(6, true);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(7, true);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(0, false);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(1, false);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(2, false);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(3, false);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(4, false);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(5, false);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(6, false);
            //Thread.Sleep(1000);
            //_robotConnector.RTDE.SetConfigurableDigitalOutput(7, false);
            //Thread.Sleep(1000);

            

            //byte[] myBytes = new byte[177];
            //myBytes[0] = 1;
            //myBytes[1] = 0;
            //myBytes[2] = 0;
            //myBytes[3] = 255;
            //myBytes[4] = 1;
            //_robotConnector.RTDE.SendData(myBytes);
            //Thread.Sleep(1000);

            //    myBytes[3] = 255;
            //myBytes[4] = 2;
            //_robotConnector.RTDE.SendData(myBytes);
            //Thread.Sleep(1000);

            //myBytes[3] = 255;
            //myBytes[4] = 4;
            //_robotConnector.RTDE.SendData(myBytes);
            //Thread.Sleep(1000);

            //myBytes[3] = 255;
            //myBytes[4] = 8;
            //_robotConnector.RTDE.SendData(myBytes);
            //Thread.Sleep(1000);

            //myBytes[3] = 255;
            //myBytes[4] = 16;
            //_robotConnector.RTDE.SendData(myBytes);
            //Thread.Sleep(1000);
        }
    }
}
