using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UniversalRobotsConnect.Types
{
    public class DigitalBits
    {
        private BitArray _digitalBits = new BitArray(8);

        public BitArray AllBits
        {
            set
            {
                for (int i = 0; i < _digitalBits.Length; i++)
                {
                    if (_digitalBits[i] != value[i])
                    {
                        _digitalBits[i] = value[i];
                        //write to log
                    }

                }

            }
            get
            {
                return _digitalBits;
                
            }
        }

       

        public bool Bit0 => _digitalBits[0];
        public bool Bit1 => _digitalBits[1];
        public bool Bit2 => _digitalBits[2];
        public bool Bit3 => _digitalBits[3];
        public bool Bit4 => _digitalBits[4];
        public bool Bit5 => _digitalBits[5];
        public bool Bit6 => _digitalBits[6];
        public bool Bit7 => _digitalBits[7];

        public bool GetBit(int bitNumber)
        {
            return _digitalBits[bitNumber];
        }

    }
}
