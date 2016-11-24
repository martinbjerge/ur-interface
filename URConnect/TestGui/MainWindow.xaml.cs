using System;
using System.Collections.Generic;
using System.IO;
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
using System.Xml;
using System.Xml.Serialization;
using UniversalRobotsConnect;
using UniversalRobotsConnect.IOs;
using UniversalRobotsConnect.Types;


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
            _robotConnector = new RobotConnector("172.16.74.129", false);
            //_robotConnector = new RobotConnector("192.168.0.3", true);
            _myRobotModel = _robotConnector.RobotModel;
            
            //_robotConnector.DashboardClient.PowerOff();

            //_robotConnector.DashboardClient.PowerOn();

            //DistanceSensor distanceSensor = new DistanceSensor("StandardAnalogInput0");
            //distanceSensor.TCP_Offset = new Vector6D(-0.012, 0.053, 0.051, 0, -0.018, 0.0);
            //distanceSensor.MaximumCurrent = 20;
            //distanceSensor.MinimumCurrent = 4;
            //distanceSensor.MaximumDistance = 0.5;
            //distanceSensor.MinimumDistance = 0.1;

            //Type[] types = new Type[] { typeof(Vector6D)};

            //XmlTextWriter textWriter = new XmlTextWriter("test.xml", Encoding.UTF8);
            //XmlSerializer xmlSerializer = new XmlSerializer(typeof(DistanceSensor), types);
            //xmlSerializer.Serialize(textWriter, distanceSensor);
            //while (true)
            //{
            //    Thread.Sleep(10000);
            //}
        }
    }
}
