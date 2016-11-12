using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;
using log4net.Config;

namespace UniversalRobotsConnect
{
    public class RobotController
    {
        private RobotConnector _robotConnector;
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        public RobotController()
        {

            _robotConnector = new RobotConnector("192.168.178.128");

            List<Command> commands = new List<Command>();

            commands.Add(new ChangeToolCommand(_robotConnector, "Get", "Soaker"));    
            commands.Add(new MoveToWorkAreaCommand(_robotConnector));
            commands.Add(new SoakCommand(/*HIGH LEVEL 3D SURFACE*/));
            commands.Add(new ChangeToolCommand(_robotConnector, "Put", "Soaker"));   
            commands.Add(new ChangeToolCommand(_robotConnector, "Get", "Sander"));    
            commands.Add(new MoveToWorkAreaCommand(_robotConnector));
            commands.Add(new SandCommand(/*HIGH LEVEL 3D SURFACE*/));
            commands.Add(new ChangeToolCommand(_robotConnector, "Put", "Sander"));   
            commands.Add(new MoveToHomePositionCommand(_robotConnector));


            foreach (Command command in commands)
            {
                command.Execute();
                while (!command.IsCompleted)
                {
                    
                }
            }
            log.Debug("NOW THE WHOLE PROGRAM IS DONE");
        }
        
    }
}















//while (true)
//{
//    //Thread.Sleep(1000);
//    ////string command = "def myprg():\nset_digital_out(0, True)\nset_digital_out(1, True)\nend\n";
//    //string command = "def myprg():\nset_digital_out(0, True)\nset_digital_out(1, True)\nend\n";
//    //byte[] commandBytes = Encoding.UTF8.GetBytes(command);
//    //_robotConnector.RealTimeClient.Send(commandBytes);
//    //Thread.Sleep(1000);
//    ////command = "def myprg():\nset_digital_out(0, False)\nset_digital_out(1, False)\nend\n";
//    //command = "def myprg():\nset_digital_out(0, False)\nset_digital_out(1, False)\nend\n";
//    //commandBytes = Encoding.UTF8.GetBytes(command);
//    //_robotConnector.RealTimeClient.Send(commandBytes);
//    //Thread.Sleep(1000);
//    string move = "def move_j():\nmovej([0.0,0.0,0.0,0.0,0.0,0.0],a=1.2,v=0.9,r=0)\nend\n";
//    byte[] commandBytes = Encoding.UTF8.GetBytes(move);
//    _robotConnector.RealTimeClient.Send(commandBytes);
//    log.Debug("Send the first move_j");
//    Thread.Sleep(6000);
//    move = "def move_j():\nmovej([0.0,0.0,0.0,0.0,0.0,0.0],a=1.2,v=0.9,r=0)\nend\n";
//    commandBytes = Encoding.UTF8.GetBytes(move);
//    _robotConnector.RealTimeClient.Send(commandBytes);
//    log.Debug("Send the second move_j");
//    Thread.Sleep(6000);
//    move = "def move_j():\nmovej([1.0,-0.5,0.0,-1.5,0.0,0.0],a=1.2,v=0.9,r=0)\nend\n";
//    commandBytes = Encoding.UTF8.GetBytes(move);
//    _robotConnector.RealTimeClient.Send(commandBytes);
//    log.Debug("Send the third move_j");
//    Thread.Sleep(6000);
//    move = "def move_j():\nmovej([1.5,0.0,-3.14,-0.5,0.0,0.0],a=1.2,v=0.9,r=0)\nend\n";
//    commandBytes = Encoding.UTF8.GetBytes(move);
//    _robotConnector.RealTimeClient.Send(commandBytes);
//    log.Debug("This was the one to go home");
//    Thread.Sleep(6000);

//}
