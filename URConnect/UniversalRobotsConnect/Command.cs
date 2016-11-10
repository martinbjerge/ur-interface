using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UniversalRobotsConnect
{
    abstract class Command
    {
       // protected Receiver receiver;

        // Constructor
        public Command(/*Receiver receiver*/)
        {
            IsCompleted = false;
        }

        public abstract void Execute();

        public abstract bool IsCompleted { get; set; }

       
    }
}
