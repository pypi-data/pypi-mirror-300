from .pca9685 import PCA9685


class MotorParam:
  """
  各モーターのパルス幅に関するパラメーターを指定するクラス
  """

  def __init__(self, min_pulse_width=1.0, max_pulse_width=2.0, input_start=0.0, input_end=100.0):
    """
    Args:
      min_pulse_width: PWMパルスの最小値[ms]
      max_pulse_width: PWMパルスの最大値[ms]
      input_start: 角度, 位置などの入力範囲の開始値. この値を入力するとmin_pulse_widthを出力する.
      input_stop: 角度, 位置などの入力範囲の終了値. この値を入力するとmax_pulse_widthを出力する.
    """
    self.min_pulse_width = min_pulse_width
    self.max_pulse_width = max_pulse_width
    self.input_start = input_start
    self.input_end = input_end

  def input2pulse_width(self, input):
    """
    入力からパルス幅を計算
    """
    if self.min_pulse_width > self.max_pulse_width:
      raise ValueError('min_pulse_width is greater than max_pulse_width')
    if (input > self.input_start and input > self.input_end) or \
      (input < self.input_start and input < self.input_end):
      raise ValueError('input out of range')

    pulse_range = self.max_pulse_width - self.min_pulse_width
    input_range = self.input_end - self.input_start
    return self.min_pulse_width + pulse_range * (input - self.input_start) / input_range

  def pulse_width2input(self, pulse_width):
    """
    パルス幅から入力を計算
    """
    pulse_range = self.max_pulse_width - self.min_pulse_width
    input_range = self.input_end - self.input_start
    return self.input_start + input_range * (pulse_width - self.min_pulse_width) / pulse_range


class Servo:
  """
  サーボモーター/ブラシレスDCモーターESC PWM制御クラス
  """

  def __init__(
      self,
      i2c_addr=0x40,
      pwm_freq_target=50.0,
      extclk=True,
      m1_param=MotorParam(),
      m2_param=MotorParam(),
      m3_param=MotorParam(),
      m4_param=MotorParam(),
      m5_param=MotorParam(),
      m6_param=MotorParam(),
  ):
    """
    Args:
      i2c_addr: PCA9685のI2Cアドレス. 7bit. 
      pwm_freq: PWM周波数の目標値[Hz]
      extclk: 高精度外部クロックを使用する
      mX_param: モーター#X用パラメーターをMotorParamクラスで指定する
    """
    self.pca9685 = PCA9685(i2c_addr=i2c_addr)
    self.pwm_freq_target = pwm_freq_target
    self.extclk = extclk
    self.m1_param = m1_param
    self.m2_param = m2_param
    self.m3_param = m3_param
    self.m4_param = m4_param
    self.m5_param = m5_param
    self.m6_param = m6_param
    self.round_input = 1
    self.round_ms = 3
    self.round_hz = 3

  def init(self, reset=True):
    """
    PCA9685をリセット後, 周波数設定してスリープ解除
    複数台使用している場合, 全てのPCA9685がリセットされるので2台目以降はreset=Falseにする

    Args:
      reset: Trueならソフトウェアリセットする
    """
    if reset:
      self.pca9685.swrst()
    self.pca9685.allcall = 0
    self.pca9685.set_pre_scale(self.pwm_freq_target)
    if self.extclk:
      self.pca9685.extclk = 1
    self.pca9685.sleep = 0

  @property
  def pwm_freq(self):
    """
    レジスターの値から実際のPWM周波数[Hz]を取得
    """
    return round(self.pca9685.clock_freq / (self.pca9685.pre_scale + 1) / 4096, self.round_hz)

  @property
  def pwm_period(self):
    """
    レジスターの値から実際のPWM周期[ms]を取得
    """
    return round((self.pca9685.pre_scale + 1) * 4096 / self.pca9685.clock_freq * 1000,
                 self.round_ms)

  def pulse_width2reg(self, pulse_width):
    """
    パルス幅からレジスター値を計算
    """
    reg = round(pulse_width / self.pwm_period * 4096)
    if reg > 4095:
      raise ValueError('pulse_width out of range')
    return reg

  def reg2pulse_width(self, reg):
    """
    レジスター値からパルス幅を計算
    """
    return reg * self.pwm_period / 4096

  """
  各モーターのパルス幅のプロパティ
  パルス幅を[ms]で指定
  m1p = 1.5 # モーター#1に1.5msパルス幅を出力
  """

  @property
  def m1p(self):
    return round(self.reg2pulse_width(self.pca9685.led0[1]), self.round_ms)

  @m1p.setter
  def m1p(self, value):
    self.pca9685.led0 = [0, self.pulse_width2reg(value)]

  @property
  def m2p(self):
    return round(self.reg2pulse_width(self.pca9685.led1[1]), self.round_ms)

  @m2p.setter
  def m2p(self, value):
    self.pca9685.led1 = [0, self.pulse_width2reg(value)]

  @property
  def m3p(self):
    return round(self.reg2pulse_width(self.pca9685.led2[1]), self.round_ms)

  @m3p.setter
  def m3p(self, value):
    self.pca9685.led2 = [0, self.pulse_width2reg(value)]

  @property
  def m4p(self):
    return round(self.reg2pulse_width(self.pca9685.led3[1]), self.round_ms)

  @m4p.setter
  def m4p(self, value):
    self.pca9685.led3 = [0, self.pulse_width2reg(value)]

  @property
  def m5p(self):
    return round(self.reg2pulse_width(self.pca9685.led4[1]), self.round_ms)

  @m5p.setter
  def m5p(self, value):
    self.pca9685.led4 = [0, self.pulse_width2reg(value)]

  @property
  def m6p(self):
    return round(self.reg2pulse_width(self.pca9685.led5[1]), self.round_ms)

  @m6p.setter
  def m6p(self, value):
    self.pca9685.led5 = [0, self.pulse_width2reg(value)]

  """
  各モーターの入力値のプロパティ
  mx_paramで指定したパラメーターに応じてパルス幅に変換されて出力される
  """

  @property
  def m1(self):
    return round(self.m1_param.pulse_width2input(self.reg2pulse_width(self.pca9685.led0[1])),
                 self.round_input)

  @m1.setter
  def m1(self, value):
    self.m1p = self.m1_param.input2pulse_width(value)

  @property
  def m2(self):
    return round(self.m2_param.pulse_width2input(self.reg2pulse_width(self.pca9685.led1[1])),
                 self.round_input)

  @m2.setter
  def m2(self, value):
    self.m2p = self.m2_param.input2pulse_width(value)

  @property
  def m3(self):
    return round(self.m3_param.pulse_width2input(self.reg2pulse_width(self.pca9685.led2[1])),
                 self.round_input)

  @m3.setter
  def m3(self, value):
    self.m3p = self.m3_param.input2pulse_width(value)

  @property
  def m4(self):
    return round(self.m4_param.pulse_width2input(self.reg2pulse_width(self.pca9685.led3[1])),
                 self.round_input)

  @m4.setter
  def m4(self, value):
    self.m4p = self.m4_param.input2pulse_width(value)

  @property
  def m5(self):
    return round(self.m5_param.pulse_width2input(self.reg2pulse_width(self.pca9685.led4[1])),
                 self.round_input)

  @m5.setter
  def m5(self, value):
    self.m5p = self.m5_param.input2pulse_width(value)

  @property
  def m6(self):
    return round(self.m6_param.pulse_width2input(self.reg2pulse_width(self.pca9685.led5[1])),
                 self.round_input)

  @m6.setter
  def m6(self, value):
    self.m6p = self.m6_param.input2pulse_width(value)
