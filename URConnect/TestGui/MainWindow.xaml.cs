using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
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
        //private RobotModel _myRobotModel;
        private RobotController _robotController;

        public MainWindow()
        {
            InitializeComponent();
            //_robotConnector = new RobotConnector("192.168.178.128");
            //_myRobotModel = _robotConnector.RobotModel;

            _robotController = new RobotController();
            
            

        }
    }
}
