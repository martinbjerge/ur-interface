using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace RobotServer
{
    class RobotConnector
    {
        public RobotModel RobotModel;
        //private RealTimeClient _realTimeClient;
        private RTDE _rtde;
        private RealTimeClient _realTimeClient;

        
        public RobotConnector(RobotModel robotModel)
        {
            RobotModel = robotModel;

            _rtde = new RTDE(RobotModel);
            _realTimeClient = new RealTimeClient(RobotModel);

            while (true)
            {
                Thread.Sleep(1000);
                // Fra RTC test i python "def myprg():\n write_output_boolean_register(0, True)\n set_digital_out(0, True)\n set_digital_out(1, True)\n\n write_output_boolean_register(1, True)\nend \n\n"
                
                string testprogramString = "def myprg():\nset_digital_out(0,False)\nset_digital_out(1,False)\nend\n";

                byte[] testprogramBytes = Encoding.UTF8.GetBytes(testprogramString);
                _realTimeClient.Send(testprogramBytes);
                Thread.Sleep(1000);
                testprogramString = "\nset_digital_out(0, True)\nset_digital_out(1, True)\nend\n";
                //testprogramString = "def myprg():\n write_output_boolean_register(0, True)\n set_digital_out(0, True)\n set_digital_out(1, True)\n\n write_output_boolean_register(1, True)\nend \n\n";
                testprogramBytes = Encoding.UTF8.GetBytes(testprogramString);
                _realTimeClient.Send(testprogramBytes);
            }
        }
    }
}
