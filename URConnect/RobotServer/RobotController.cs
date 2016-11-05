using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RobotServer
{
    public class RobotController
    {
        private static RobotModel _robotModel;
        private RobotConnector _robotConnector;

        public RobotController()
        {
            _robotModel = new RobotModel();
            _robotConnector = new RobotConnector(_robotModel);
            Debug.WriteLine("I'm back!");
        }

        public string GetActualDigitalOutputBits()
        {
            return _robotModel.ActualDigitalOutputBits.ToString();
            //return _robotModel.RobotTimestamp.ToString();
        }


    }
}
