import smbus2


class PCA9685:
  """
  PWMドライバー PCA9685制御クラス
  """

  def __init__(self, i2c_addr, i2c_bus=1):
    """
    Args:
      i2c_addr: デバイスのI2Cアドレス. 7bit. 
      i2c_bus: I2Cバス番号
    """
    self.i2c_addr = i2c_addr
    self.bus = smbus2.SMBus(i2c_bus)
    self.clock_freq = 25000000  # クロック周波数[Hz]

  ##############################################
  # Direct Register Access

  def read_register(self, addr, length=1):
    """
    I2Cで指定アドレスからデータを読み出す
    2バイト以上の場合は自動的にauto incrementをセット

    Args:
      addr: 読み出しアドレス. 8bit. 
      length: 読み出しデータの長さ. バイト数.
    
    Returns:
      list: 読み出しデータのリスト
    """
    if length > 1:
      if self.ai == 0:
        self.ai = 1

    msg_write = smbus2.i2c_msg.write(self.i2c_addr, [addr & 0xFF])
    msg_read = smbus2.i2c_msg.read(self.i2c_addr, length)
    self.bus.i2c_rdwr(msg_write, msg_read)
    return list(msg_read)

  def write_register(self, addr, data):
    """
    I2Cで指定アドレスにデータを書き込む
    2バイト以上の場合は自動的にauto incrementをセット

    Args:
      addr: 書き込みアドレス. 8bit. 
      data(list): 書き込みデータのリスト. 
    """
    if len(data) > 1:
      if self.ai == 0:
        self.ai = 1

    write_data = [addr & 0xFF]
    for b in data:
      write_data.append(b)

    msg_write = smbus2.i2c_msg.write(self.i2c_addr, write_data)
    self.bus.i2c_rdwr(msg_write)

  def swrst(self):
    """
    ソフトウェアリセット
    """
    msg_write = smbus2.i2c_msg.write(0, [0x6])
    self.bus.i2c_rdwr(msg_write)

  def get_bits(self, data, msb, lsb):
    """
    dataの指定ビットの値を返す
    """
    if msb < lsb:
      raise ValueError('lsb is larger than msb')
    length = msb - lsb + 1
    data = data >> lsb
    data &= (2**length - 1)
    return data

  def set_bits(self, data, msb, lsb, value):
    """
    8bit幅のdataの指定ビットにvalueをセットした値を返す
    """
    if msb < lsb:
      raise ValueError('lsb is larger than msb')

    length = msb - lsb + 1
    if value >= 2**length:
      raise ValueError('value exceeds length')

    # 指定ビットを0にする
    for i in range(lsb, msb + 1):
      data &= (0xFF - (1 << i))

    data ^= (value << lsb)
    return data

  def get_register_bits(self, addr, msb, lsb):
    """
    指定レジスターの指定ビットを返す
    """
    return self.get_bits(self.read_register(addr)[0], msb, lsb)

  def set_register_bits(self, addr, msb, lsb, value):
    """
    指定レジスター(8bit)の指定ビットにvalueをセットして書き込む
    一度読み出して, レジスターの未指定ビットは変更前と同じ値を書き込む
    """
    data = self.read_register(addr)[0]
    data = self.set_bits(data, msb, lsb, value)
    self.write_register(addr, [data])

  def get_led(self, addr):
    """
    LEDのON, OFFパラメーターを読み出す

    Args:
      addr: 先頭レジスター(LEDx_ON_L)アドレス. 8bit. 
    
    Returns:
      list: 対象LEDの[ONの値, OFFの値]
    """
    data = self.read_register(addr, 4)
    return data[0] + (data[1] << 8), data[2] + (data[3] << 8)

  def set_led(self, addr, data):
    """
    LEDのON, OFFパラメーターを書き込む

    Args:
      addr: 先頭レジスター(LEDx_ON_L)アドレス. 8bit. 
      data: リスト. 対象LEDの[ONの値, OFFの値]
    """
    data = self.write_register(
        addr, [data[0] & 0xFF, (data[0] >> 8) & 0xFF, data[1] & 0xFF, (data[1] >> 8) & 0xFF])

  def set_pre_scale(self, pwm_freq_target):
    """
    周期から最も近いPRE_SCALEレジスターを設定

    Args:
      pwm_freq_target: PWM周波数[Hz]
    """
    pre_scale = round(self.clock_freq / pwm_freq_target / 4096 - 1)
    if pre_scale < 3 or pre_scale > 255:
      raise ValueError('pwm_freq {} out of range'.format(pwm_freq_target))
    self.pre_scale = pre_scale

  ###################
  # MODE1 0x0
  @property
  def mode1(self):
    return self.read_register(0x0)[0]

  @mode1.setter
  def mode1(self, value):
    self.write_register(0x0, [value])

  @property
  def allcall(self):
    return self.get_register_bits(0x0, 0, 0)

  @allcall.setter
  def allcall(self, value):
    self.set_register_bits(0x0, 0, 0, value)

  @property
  def sub3(self):
    return self.get_register_bits(0x0, 1, 1)

  @sub3.setter
  def sub3(self, value):
    self.set_register_bits(0x0, 1, 1, value)

  @property
  def sub2(self):
    return self.get_register_bits(0x0, 2, 2)

  @sub2.setter
  def sub2(self, value):
    self.set_register_bits(0x0, 2, 2, value)

  @property
  def sub1(self):
    return self.get_register_bits(0x0, 3, 3)

  @sub1.setter
  def sub1(self, value):
    self.set_register_bits(0x0, 3, 3, value)

  @property
  def sleep(self):
    return self.get_register_bits(0x0, 4, 4)

  @sleep.setter
  def sleep(self, value):
    self.set_register_bits(0x0, 4, 4, value)

  @property
  def ai(self):
    return self.get_register_bits(0x0, 5, 5)

  @ai.setter
  def ai(self, value):
    self.set_register_bits(0x0, 5, 5, value)

  @property
  def extclk(self):
    return self.get_register_bits(0x0, 6, 6)

  @extclk.setter
  def extclk(self, value):
    self.set_register_bits(0x0, 6, 6, value)

  @property
  def restart(self):
    return self.get_register_bits(0x0, 7, 7)

  @restart.setter
  def restart(self, value):
    self.set_register_bits(0x0, 7, 7, value)

  ###################
  # MODE2 0x1
  @property
  def mode2(self):
    return self.read_register(0x1)[0]

  @mode2.setter
  def mode2(self, value):
    self.write_register(0x1, [value & 0x1F])

  @property
  def outne(self):
    return self.get_register_bits(0x1, 1, 0)

  @outne.setter
  def outne(self, value):
    self.set_register_bits(0x1, 1, 0, value)

  @property
  def outdrv(self):
    return self.get_register_bits(0x1, 2, 2)

  @outdrv.setter
  def outdrv(self, value):
    self.set_register_bits(0x1, 2, 2, value)

  @property
  def och(self):
    return self.get_register_bits(0x1, 3, 3)

  @och.setter
  def och(self, value):
    self.set_register_bits(0x1, 3, 3, value)

  @property
  def invrt(self):
    return self.get_register_bits(0x1, 4, 4)

  @invrt.setter
  def invrt(self, value):
    self.set_register_bits(0x1, 4, 4, value)

  ###################
  # LED0-15 0x06 - 0x45
  #  value[0]: ONの値, value[1]: OFFの値を指定

  @property
  def led0(self):
    return self.get_led(0x6)

  @led0.setter
  def led0(self, value):
    self.set_led(0x6, value)

  @property
  def led1(self):
    return self.get_led(0xA)

  @led1.setter
  def led1(self, value):
    self.set_led(0xA, value)

  @property
  def led2(self):
    return self.get_led(0xE)

  @led2.setter
  def led2(self, value):
    self.set_led(0xE, value)

  @property
  def led3(self):
    return self.get_led(0x12)

  @led3.setter
  def led3(self, value):
    self.set_led(0x12, value)

  @property
  def led4(self):
    return self.get_led(0x16)

  @led4.setter
  def led4(self, value):
    self.set_led(0x16, value)

  @property
  def led5(self):
    return self.get_led(0x1A)

  @led5.setter
  def led5(self, value):
    self.set_led(0x1A, value)

  @property
  def led6(self):
    return self.get_led(0x1E)

  @led6.setter
  def led6(self, value):
    self.set_led(0x1E, value)

  @property
  def led7(self):
    return self.get_led(0x22)

  @led7.setter
  def led7(self, value):
    self.set_led(0x22, value)

  @property
  def led8(self):
    return self.get_led(0x26)

  @led8.setter
  def led8(self, value):
    self.set_led(0x26, value)

  @property
  def led9(self):
    return self.get_led(0x2A)

  @led9.setter
  def led9(self, value):
    self.set_led(0x2A, value)

  @property
  def led10(self):
    return self.get_led(0x2E)

  @led10.setter
  def led10(self, value):
    self.set_led(0x2E, value)

  @property
  def led11(self):
    return self.get_led(0x32)

  @led11.setter
  def led11(self, value):
    self.set_led(0x32, value)

  @property
  def led12(self):
    return self.get_led(0x36)

  @led12.setter
  def led12(self, value):
    self.set_led(0x36, value)

  @property
  def led13(self):
    return self.get_led(0x3A)

  @led13.setter
  def led13(self, value):
    self.set_led(0x3A, value)

  @property
  def led14(self):
    return self.get_led(0x3E)

  @led14.setter
  def led14(self, value):
    self.set_led(0x3E, value)

  @property
  def led15(self):
    return self.get_led(0x42)

  @led15.setter
  def led15(self, value):
    self.set_led(0x42, value)

  def all_led(self, value):
    self.set_led(0xFA, value)

  all_led = property(None, all_led)  # setterのみ

  ###################
  # PRE_SCALE 0xFE

  @property
  def pre_scale(self):
    return self.read_register(0xFE)[0]

  @pre_scale.setter
  def pre_scale(self, value):
    self.write_register(0xFE, [value])

  ###################
  # Print Functions

  def print_config_reg(self):
    print('MODE1: {:#02x}'.format(self.mode1))
    print(' RESTART: {}'.format(self.restart))
    print(' EXTCLK: {}'.format(self.extclk))
    print(' AI: {}'.format(self.ai))
    print(' SLEEP: {}'.format(self.sleep))
    print(' SUB1: {}'.format(self.sub1))
    print(' SUB2 {}'.format(self.sub2))
    print(' SUB3 {}'.format(self.sub3))
    print(' ALLCALL {}'.format(self.allcall))

    print('MODE2: {:#02x}'.format(self.mode2))
    print(' OUTNE: {}'.format(self.outne))
    print(' OUTDRV: {}'.format(self.outdrv))
    print(' OCH: {}'.format(self.och))
    print(' INVRT: {}'.format(self.invrt))

    print('PRE_SCALE: {}'.format(self.pre_scale))

  def print_led_reg(self):
    print('LED0:{}'.format(self.led0))
    print('LED1:{}'.format(self.led1))
    print('LED2:{}'.format(self.led2))
    print('LED3:{}'.format(self.led3))
    print('LED4:{}'.format(self.led4))
    print('LED5:{}'.format(self.led5))
    print('LED6:{}'.format(self.led6))
    print('LED7:{}'.format(self.led7))
    print('LED8:{}'.format(self.led8))
    print('LED9:{}'.format(self.led9))
    print('LED10:{}'.format(self.led10))
    print('LED11:{}'.format(self.led11))
    print('LED12:{}'.format(self.led12))
    print('LED13:{}'.format(self.led13))
    print('LED14:{}'.format(self.led14))
    print('LED15:{}'.format(self.led15))
