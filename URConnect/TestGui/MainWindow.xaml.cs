using System;
using System.Collections.Generic;
using System.Diagnostics;
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
            //_robotConnector = new RobotConnector("192.168.0.3", false);
            _myRobotModel = _robotConnector.RobotModel;
            



            //_robotConnector.RealTimeClient.Send("set_tcp(p[0.023, 0.053, 0.15, 0.000, 0.000, 0.000])");



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
            Thread.Sleep(2000);

            



            
        }

        private async void button_Click(object sender, RoutedEventArgs e)
        {
            //_robotConnector.RealTimeClient.Send("set_tcp(p[0.023, 0.053, 0.15, 0.000, 0.000, 0.000])");
            DateTime startTime = DateTime.Now;
            _robotConnector.RealTimeClient.Send("def move_l():\nmovel(p[0.6, 0.406, -0.0302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2, 0.405, -0.0302, 2.8341, 0.0076, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6, 0.4167, -0.0336, 2.8142, 0.01, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2, 0.4159, -0.0339, 2.7911, 0.0123, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6, 0.4273, -0.0375, 2.7664, 0.0144, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2, 0.4265, -0.0381, 2.7355, 0.0167, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6, 0.4378, -0.042, 2.7028, 0.0187, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2, 0.4363, -0.0427, 2.6655, 0.0205, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6001, 0.4472, -0.0469, 2.6236, 0.0222, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2001, 0.4456, -0.048, 2.574, 0.0238, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6001, 0.4563, -0.0526, 2.5192, 0.0251, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2001, 0.4539, -0.054, 2.459, 0.0261, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6001, 0.464, -0.0589, 2.3888, 0.027, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2001, 0.4611, -0.0607, 2.3047, 0.0276, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6001, 0.4702, -0.0659, 2.1975, 0.028, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2002, 0.466, -0.0676, 2.0403, 0.0278, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6002, 0.4732, -0.0716, 1.7941, 0.0265, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2002, 0.467, -0.0705, 1.4085, 0.0231, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6002, 0.4732, -0.0723, 1.0041, 0.0184, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2002, 0.4656, -0.0722, 0.7205, 0.0147, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6002, 0.4689, -0.076, 0.552, 0.0124, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2001, 0.4587, -0.0764, 0.4503, 0.0109, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6001, 0.4604, -0.0801, 0.38, 0.0099, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2001, 0.4492, -0.0803, 0.331, 0.0092, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6001, 0.4502, -0.0836, 0.2931, 0.0086, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2001, 0.4384, -0.0835, 0.2637, 0.0082, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6001, 0.4392, -0.0866, 0.2406, 0.0078, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2001, 0.4276, -0.0862, 0.2225, 0.0076, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6001, 0.4281, -0.0891, 0.2061, 0.0073, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2001, 0.4155, -0.0887, 0.1913, 0.0071, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6001, 0.416, -0.0915, 0.1796, 0.0069, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.2001, 0.4045, -0.0907, 0.1706, 0.0068, -0.0], a = 0.4, v = 0.4, r = 0)\nmovel(p[0.6001, 0.4054, -0.0933, 0.1622, 0.0066, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");
            DateTime finishedSendTime = DateTime.Now;
            while (_robotConnector.RobotModel.RuntimeState != RuntimeState.Running)
            {
                
            }

            DateTime robotStartRunningTime = DateTime.Now;
            TimeSpan timeToGoIntoRunningState = robotStartRunningTime - finishedSendTime;
            if ( timeToGoIntoRunningState.Ticks > 0)
            {
                Debug.WriteLine($"Timespan was {timeToGoIntoRunningState.Ticks/10} microseconds");
            }

            //await Task.Delay(3000);
            //_robotConnector.RealTimeClient.Send("def move_l():\nmovel(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //Debug.WriteLine("just send second move");

            //while (_robotConnector.RobotModel.RuntimeState != RuntimeState.Idle)
            //{

            //}
            DateTime robotFinishedMoveTime = DateTime.Now;

            Debug.WriteLine($"Time to go into running state: {robotStartRunningTime-finishedSendTime}" );
            //Debug.WriteLine($"Time to finish running state: {robotStartRunningTime-robotFinishedMoveTime}" );
            Debug.WriteLine($"Time to actually move after running state: {robotFinishedMoveTime-robotStartRunningTime}" );

        }

        private void button1_Click(object sender, RoutedEventArgs e)
        {
            _robotConnector.RealTimeClient.Send("def move_l():\nmovel(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");

        }
    }
}
