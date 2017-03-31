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
using PhoenixModbus;
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
        private HFI _hfi;
        //private RobotModel _myRobotModel;
       

        public MainWindow()
        {
            InitializeComponent();
            //_robotConnector = new RobotConnector("192.168.1.148", false);
            //_robotConnector = new RobotConnector("172.16.74.129", false);
            //_robotConnector = new RobotConnector("192.168.0.3", false);
            //_myRobotModel = _robotConnector.RobotModel;

            _hfi = new HFI("192.168.1.50");

            _hfi.SetDigitalOut(0, true);
            _hfi.SetDigitalOut(1, true);
            _hfi.SetDigitalOut(2, true);
            _hfi.SetDigitalOut(3, true);
            
            
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
            //Thread.Sleep(2000);






        }

        private async void button_Click(object sender, RoutedEventArgs e)
        {
            //_robotConnector.RealTimeClient.Send("set_tcp(p[0.023, 0.053, 0.15, 0.000, 0.000, 0.000])");

            string movetype = "movel";
            string velocity = "0.4";
            
            _robotConnector.RealTimeClient.SendProgram($"def {movetype}():\n{movetype}(p[0.6, 0.606, -0.0302, 2.8509, 0.0054, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2, 0.605, -0.0302, 2.8341, 0.0076, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.6, 0.6167, -0.0336, 2.8142, 0.01, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2, 0.6159, -0.0339, 2.7911, 0.0123, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.6, 0.6273, -0.0375, 2.7664, 0.0144, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2, 0.6265, -0.0381, 2.7355, 0.0167, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.6, 0.6378, -0.042, 2.7028, 0.0187, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2, 0.6363, -0.0427, 2.6655, 0.0205, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6472, -0.0469, 2.6236, 0.0222, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6456, -0.048, 2.574, 0.0238, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6563, -0.0526, 2.5192, 0.0251, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6539, -0.054, 2.459, 0.0261, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.664, -0.0589, 2.3888, 0.027, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6611, -0.0507, 2.3047, 0.0276, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6702, -0.0659, 2.1975, 0.028, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2002, 0.666, -0.0476, 2.0403, 0.0278, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5002, 0.6732, -0.0716, 1.7941, 0.0265, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2002, 0.667, -0.0505, 1.4085, 0.0231, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5002, 0.6732, -0.0723, 1.0041, 0.0184, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2002, 0.6656, -0.0722, 0.5205, 0.0147, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5002, 0.6689, -0.056, 0.552, 0.0124, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6587, -0.0764, 0.4503, 0.0109, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.6, 0.6604, -0.0501, 0.38, 0.0099, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6492, -0.0803, 0.331, 0.0092, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6502, -0.0536, 0.2931, 0.0086, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6384, -0.0535, 0.2637, 0.0082, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6392, -0.0466, 0.2406, 0.0078, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6276, -0.0462, 0.2225, 0.0076, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6281, -0.0491, 0.2061, 0.0073, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.6155, -0.0487, 0.1913, 0.0071, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.616, -0.0915, 0.1796, 0.0069, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.2001, 0.4645, -0.0907, 0.1706, 0.0068, -0.0], a = 0.4, v = {velocity}, r = 0)\n{movetype}(p[0.5, 0.6054, -0.0533, 0.1622, 0.0066, -0.0], a = 0.4, v = {velocity}, r = 0)\nstopl(0.4)\nend\n");
            DateTime finishedSendTime = DateTime.Now;
            while (_robotConnector.RobotModel.RuntimeState != RuntimeState.Running)
            {
                await Task.Delay(10);
            }

            DateTime robotStartRunningTime = DateTime.Now;
            TimeSpan timeToGoIntoRunningState = robotStartRunningTime - finishedSendTime;
            if ( timeToGoIntoRunningState.Ticks > 0)
            {
                Debug.WriteLine($"Timespan was {timeToGoIntoRunningState.Ticks/10} microseconds");
            }
            Debug.WriteLine($"Time to go into running state: {robotStartRunningTime - finishedSendTime}");
            //await Task.Delay(3000);
            //_robotConnector.RealTimeClient.Send("def move_l():\n{movetype}(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = {velocity}, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //Debug.WriteLine("just send second move");

            while (_robotConnector.RobotModel.RuntimeState != RuntimeState.Idle)
            {

            }
            DateTime robotFinishedMoveTime = DateTime.Now;

            Debug.WriteLine($"Time to go into running state: {robotStartRunningTime-finishedSendTime}" );
            Debug.WriteLine($"Time to finish running state: {robotStartRunningTime-robotFinishedMoveTime}" );
            Debug.WriteLine($"Time to actually move after running state: {robotFinishedMoveTime-robotStartRunningTime}" );

        }

        private void button1_Click(object sender, RoutedEventArgs e)
        {
            

            _robotConnector.RealTimeClient.SendProgram("def move_j():\nmovej( [0.321, -1.278, -1.967, -1.474, 1.578, 1.422], a = 1.4, v = 0.5,  r = 0)\nmovej( [-0.336, -1.471, -1.813, -1.44, 1.57, 0.765], a = 1.4, v = 0.5,  r = 0)\nmovej( [-0.335, -1.582, -2.072, -1.07, 1.57, 0.764], a = 1.4, v = 0.5,  r = 0)\nstopl(1.4, 1.4)\nend\n");


            //string movetype = "movel";
            //Debug.WriteLine("Button1 click");
            //_robotConnector.RealTimeClient.SendProgram($"def move_l():\n{movetype}(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //Debug.WriteLine("First MoveL done");
            //_robotConnector.RealTimeClient.SendProgram($"def move_l():\n{movetype}(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //Debug.WriteLine("Second MoveL done");
            //_robotConnector.RealTimeClient.SendProgram($"def move_l():\n{movetype}(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //Debug.WriteLine("Third MoveL done");
            //_robotConnector.RealTimeClient.SendProgram($"def move_l():\n{movetype}(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //Debug.WriteLine("Fourth First MoveL done");
            //_robotConnector.RealTimeClient.SendProgram($"def move_l():\n{movetype}(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //Debug.WriteLine("Fifth MoveL done");
            //_robotConnector.RealTimeClient.SendProgram($"def move_l():\n{movetype}(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //Debug.WriteLine("Sixth MoveL");
            //_robotConnector.RealTimeClient.SendProgram($"def move_l():\n{movetype}(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //Debug.WriteLine("Seventh MoveL");
            //_robotConnector.RealTimeClient.SendProgram($"def move_l():\n{movetype}(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //Debug.WriteLine("Eigth MoveL");
            //_robotConnector.RealTimeClient.SendProgram($"def move_l():\n{movetype}(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");
            //Debug.WriteLine("Ninth MoveL");
            //_robotConnector.RealTimeClient.SendProgram($"def move_l():\n{movetype}(p[0.1, -0.706, -0.4302, 2.8509, 0.0054, -0.0], a = 0.4, v = 0.4, r = 0)\nstopl(0.4, 0.4)\nend\n");

            //Debug.WriteLine($"Returned from {movetype} and got all 10");
        }
    }
}
