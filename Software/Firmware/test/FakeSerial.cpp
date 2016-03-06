/**
 * OpenExposer firmware
 *
 *  Copyright 2016 by Christoph Emonds <info@christoph-emonds.de>
 *
 * This file is part of OpenExposer firmware.
 *
 * OpenExposer firmware is free software: you can redistribute
 * it and/or modify it under the terms of the GNU General Public
 * License as published by the Free Software Foundation, either
 * version 3 of the License, or (at your option) any later version.
 *
 * OpenExposer firmware is distributed in the hope that it will
 * be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
 * of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
 *
 * @license GPL-3.0+ <http://opensource.org/licenses/GPL-3.0>
 */

#include "FakeSerial.h"

FakeSerial Serial;

// Public Methods //////////////////////////////////////////////////////////////

size_t FakeSerial::print(const char [])
{
  return 0;
}

size_t FakeSerial::print(char)
{
  return 0;
}

size_t FakeSerial::print(unsigned char, int)
{
  return 0;
}

size_t FakeSerial::print(int, int)
{
  return 0;
}

size_t FakeSerial::print(unsigned int, int)
{
  return 0;
}

size_t FakeSerial::print(long, int)
{
  return 0;
}

size_t FakeSerial::print(unsigned long, int)
{
  return 0;
}

size_t FakeSerial::print(double, int)
{
  return 0;
}

size_t FakeSerial::println(void)
{
  return 0;
}

size_t FakeSerial::println(const char[])
{
  return 0;
}

size_t FakeSerial::println(char)
{
  return 0;
}

size_t FakeSerial::println(unsigned char, int)
{
  return 0;
}

size_t FakeSerial::println(int, int)
{
  return 0;
}

size_t FakeSerial::println(unsigned int, int)
{
  return 0;
}

size_t FakeSerial::println(long, int)
{
  return 0;
}

size_t FakeSerial::println(unsigned long, int)
{
  return 0;
}

size_t FakeSerial::println(double, int)
{
  return 0;
}
