using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect.Types
{
    public class OutputBitRegister
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        private BitArray _outputBitRegisters = new BitArray(64);

        internal BitArray SetOutputBitRegisters0to31
        {
            set
            {
                for (int i = 0; i < 31; i++)
                {
                    if (_outputBitRegisters[i] != value[i])
                    {
                        _outputBitRegisters[i] = value[i];
                        //log.Info($"{RobotTimestamp}, OutputBitRegister{i} {(bool)value[i]}");
                    }
                    i++;
                }
            }
        }

        internal BitArray SetOutputBitRegisters32to63
        {
            set
            {
                for (int i = 32; i < 63; i++)
                {
                    if (_outputBitRegisters[i] != value[i - 32])
                    {
                        _outputBitRegisters[i] = value[i-32];
                        //log.Info($"{RobotTimestamp}, OutputBitRegister{i} {(bool)value[i - 32]}");
                    }
                    i++;
                }
            }
        }

        public bool Bit0 => _outputBitRegisters[0];

        public bool Bit1 => _outputBitRegisters[1];

        public bool Bit2 => _outputBitRegisters[2];

        public bool Bit3 => _outputBitRegisters[3];

        public bool Bit4 => _outputBitRegisters[4];

        public bool Bit5 => _outputBitRegisters[5];

        public bool Bit6 => _outputBitRegisters[6];
        public bool Bit7 => _outputBitRegisters[7];
        public bool Bit8 => _outputBitRegisters[8];
        public bool Bit9 => _outputBitRegisters[9];
        public bool Bit10 => _outputBitRegisters[10];
        public bool Bit11 => _outputBitRegisters[11];
        public bool Bit12 => _outputBitRegisters[12];
        public bool Bit13 => _outputBitRegisters[13];
        public bool Bit14 => _outputBitRegisters[14];
        public bool Bit15 => _outputBitRegisters[15];
        public bool Bit16 => _outputBitRegisters[16];
        public bool Bit17 => _outputBitRegisters[17];
        public bool Bit18 => _outputBitRegisters[18];
        public bool Bit19 => _outputBitRegisters[19];
        public bool Bit20 => _outputBitRegisters[20];
        public bool Bit21 => _outputBitRegisters[21];
        public bool Bit22 => _outputBitRegisters[22];
        public bool Bit23 => _outputBitRegisters[23];
        public bool Bit24 => _outputBitRegisters[24];
        public bool Bit25 => _outputBitRegisters[25];
        public bool Bit26 => _outputBitRegisters[26];
        public bool Bit27 => _outputBitRegisters[27];
        public bool Bit28 => _outputBitRegisters[28];
        public bool Bit29 => _outputBitRegisters[29];
        public bool Bit30 => _outputBitRegisters[30];
        public bool Bit31 => _outputBitRegisters[31];
        public bool Bit32 => _outputBitRegisters[32];
        public bool Bit33 => _outputBitRegisters[33];
        public bool Bit34 => _outputBitRegisters[34];
        public bool Bit35 => _outputBitRegisters[35];
        public bool Bit36 => _outputBitRegisters[36];
        public bool Bit37 => _outputBitRegisters[37];
        public bool Bit38 => _outputBitRegisters[38];
        public bool Bit39 => _outputBitRegisters[39];
        public bool Bit40 => _outputBitRegisters[40];
        public bool Bit41 => _outputBitRegisters[41];
        public bool Bit42 => _outputBitRegisters[42];
        public bool Bit43 => _outputBitRegisters[43];
        public bool Bit44 => _outputBitRegisters[44];
        public bool Bit45 => _outputBitRegisters[45];
        public bool Bit46 => _outputBitRegisters[46];
        public bool Bit47 => _outputBitRegisters[47];
        public bool Bit48 => _outputBitRegisters[48];
        public bool Bit49 => _outputBitRegisters[49];
        public bool Bit50 => _outputBitRegisters[50];
        public bool Bit51 => _outputBitRegisters[51];
        public bool Bit52 => _outputBitRegisters[52];
        public bool Bit53 => _outputBitRegisters[53];
        public bool Bit54 => _outputBitRegisters[54];
        public bool Bit55 => _outputBitRegisters[55];
        public bool Bit56 => _outputBitRegisters[56];
        public bool Bit57 => _outputBitRegisters[57];
        public bool Bit58 => _outputBitRegisters[58];
        public bool Bit59 => _outputBitRegisters[59];
        public bool Bit60 => _outputBitRegisters[60];
        public bool Bit61 => _outputBitRegisters[61];
        public bool Bit62 => _outputBitRegisters[62];
        public bool Bit63 => _outputBitRegisters[63];
    }
}
