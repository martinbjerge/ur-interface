using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Remoting.Channels;
using System.Text;
using System.Threading.Tasks;
using PhoenixContact.HFI.Inline;

namespace PhoenixModbus
{
    public sealed class HFI : IDisposable
    {
        // Information:
        // If you are using this programm you have to disable the
        // PnP Mode of the ETH BK DI8 DO4

        public Queue<Exception> ExceptionList { get; private set; }

        public Controller_IBS_ETH Controller { get; private set; }

        //VarInput   MODULE_2_IN  = new VarInput(0,PD_Length.Word,8,0);
        VarInput IN_Bit_0 = new VarInput(0, PD_Length.Word, 1, 0, "DigitalInput0");
        VarInput IN_Bit_1 = new VarInput(0, PD_Length.Word, 1, 1, "DigitalInput1");
        VarInput IN_Bit_2 = new VarInput(0, PD_Length.Word, 1, 2, "DigitalInput2");
        VarInput IN_Bit_3 = new VarInput(0, PD_Length.Word, 1, 3, "DigitalInput3");
        VarInput IN_Bit_4 = new VarInput(0, PD_Length.Word, 1, 4, "DigitalInput4");
        VarInput IN_Bit_5 = new VarInput(0, PD_Length.Word, 1, 5, "DigitalInput5");
        VarInput IN_Bit_6 = new VarInput(0, PD_Length.Word, 1, 6, "DigitalInput6");
        VarInput IN_Bit_7 = new VarInput(0, PD_Length.Word, 1, 7, "DigitalInput7");

        VarInput MODULE_3_IN = new VarInput(2, PD_Length.LWord, 64, 0);
        VarInput MODULE_4_IN = new VarInput(10, PD_Length.DWord, 32, 0);



        //private VarOutput MODULE_1_OUT = new VarOutput(0, PD_Length.Word, 4, 0);
        VarOutput OUT_Bit_0 = new VarOutput(0, PD_Length.Word, 1, 0, "DigitalOutput0");
        VarOutput OUT_Bit_1 = new VarOutput(0, PD_Length.Word, 1, 1, "DigitalOutput1");
        VarOutput OUT_Bit_2 = new VarOutput(0, PD_Length.Word, 1, 2, "DigitalOutput2");
        VarOutput OUT_Bit_3 = new VarOutput(0, PD_Length.Word, 1, 3, "DigitalOutput3");


        VarOutput MODULE_3_OUT = new VarOutput(2, PD_Length.LWord, 64, 0);
        VarOutput MODULE_4_OUT = new VarOutput(10, PD_Length.DWord, 32, 0);



        /// <summary>
        /// Constructor
        /// </summary>
        public HFI(string ipAddress)
        {
            ExceptionList = new Queue<Exception>();

            Controller = new Controller_IBS_ETH("ETH BK DI8 DO4");
            Controller.Description = "ETH BK DI8 DO4";
            Controller.Startup = ControllerStartup.PhysicalConfiguration;
            Controller.Connection = "192.168.1.50";
            Controller.UpdateProcessDataCycleTime = 20;
            Controller.UpdateMailboxTime = 50;

            // The Controller.Configuration property contains special configurations for the controller
            //Controller.Configuration.DNS_NameResolution     = true;
            //Controller.Configuration.EnableIBS_Indications  = true;
            //Controller.Configuration.Read_IBS_Cycletime     = false;
            //Controller.Configuration.UpdateControllerState  = 100;
            
            //Controller.AddObject(MODULE_2_IN);
            Controller.AddObject(IN_Bit_0);
            Controller.AddObject(IN_Bit_1);
            Controller.AddObject(IN_Bit_2);
            Controller.AddObject(IN_Bit_3);
            Controller.AddObject(IN_Bit_4);
            Controller.AddObject(IN_Bit_5);
            Controller.AddObject(IN_Bit_6);
            Controller.AddObject(IN_Bit_7);

            Controller.AddObject(MODULE_3_IN);
            Controller.AddObject(MODULE_4_IN);

            
            //Controller.AddObject(MODULE_1_OUT);
            Controller.AddObject(OUT_Bit_0);
            Controller.AddObject(OUT_Bit_1);
            Controller.AddObject(OUT_Bit_2);
            Controller.AddObject(OUT_Bit_3);

            Controller.AddObject(MODULE_3_OUT);
            Controller.AddObject(MODULE_4_OUT);
            
            Controller.OnUpdateProcessData += Controller_OnUpdateProcessData;
            Controller.OnUpdateMailbox += Controller_OnUpdateMailbox;
            Controller.OnException += Controller_OnException;

            Controller.Enable();
        }

        public bool GetDigitalInput(int inputNumber)
        {
            switch (inputNumber)
            {
                case 0:
                    return IN_Bit_0.State;
                case 1:
                    return IN_Bit_1.State;
                case 2:
                    return IN_Bit_2.State;
                case 3:
                    return IN_Bit_3.State;
                case 4:
                    return IN_Bit_4.State;
                case 5:
                    return IN_Bit_5.State;
                case 6:
                    return IN_Bit_6.State;
                case 7:
                    return IN_Bit_7.State;
            }
            throw new ArgumentOutOfRangeException();
        }

        public bool SetDigitalOut(int outputNumber, bool state)
        {
            switch (outputNumber)
            {
                case 0:
                    return OUT_Bit_0.State = state;
                case 1:
                    return OUT_Bit_1.State = state;
                case 2:
                    return OUT_Bit_2.State = state;
                case 3:
                    return OUT_Bit_3.State = state;
            }
            throw new ArgumentOutOfRangeException();
        }
    

        /// <summary>
        /// Called once for each bus cycle
        /// </summary>
        /// <param name="Sender"></param>
        private void Controller_OnUpdateProcessData(object Sender)
        {
            
        }

        /// <summary>
        /// Called once for each mailbox cycle
        /// </summary>
        /// <param name="Sender"></param>
        private void Controller_OnUpdateMailbox(object Sender)
        {
            
        }

        /// <summary>
        ///  Called whenever an error occurs in the controller object
        /// </summary>
        /// <param name="ExceptionData"></param>
        private void Controller_OnException(Exception ExceptionData)
        {
            
            ExceptionList.Enqueue(ExceptionData);
            
        }



        public void Dispose()
        {
            if (this.Controller != null)
            {
                if (this.Controller.Connect || this.Controller.Error)
                {
                    this.Controller.Disable();

                    while (this.Controller.Connect || this.Controller.Error)
                    {
                        System.Threading.Thread.Sleep(10);
                    }
                }

                this.Controller.Dispose();
            }
        }
    }
}
