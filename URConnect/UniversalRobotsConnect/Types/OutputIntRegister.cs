using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect.Types
{
    public class OutputIntRegister
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);
        //private int[] _outputIntRegisters = new int[24];

        //public int Register0
        //{
        //    get { return _outputIntRegisters[0]; }
        //    set { _outputIntRegisters[0] = value; }
        //}
        public int Register0 { get; set; }
        public int Register1 { get; set; }
        public int Register2 { get; set; }
        public int Register3 { get; set; }
        public int Register4 { get; set; }
        public int Register5 { get; set; }
        public int Register6 { get; set; }
        public int Register7 { get; set; }
        public int Register8 { get; set; }
        public int Register9 { get; set; }
        public int Register10 { get; set; }
        public int Register11 { get; set; }
        public int Register12 { get; set; }
        public int Register13 { get; set; }
        public int Register14 { get; set; }
        public int Register15 { get; set; }
        public int Register16 { get; set; }
        public int Register17 { get; set; }
        public int Register18 { get; set; }
        public int Register19 { get; set; }
        public int Register20 { get; set; }
        public int Register21 { get; set; }
        public int Register22 { get; set; }
        public int Register23 { get; set; }
    }
}
