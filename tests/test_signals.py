from guiserver import signals

test_x = [0, 0.035063563449037, 0.072549588071957, 0.0988682205087, 0.125121037945465, 0.151405663343619, 0.203981137447114, 0.229248145728446, 0.254357698360861, 0.280585622090709, 0.302243616666074, 0.324071100849019, 0.350470973384977, 0.376773577279248, 0.403066500739096, 0.429359423720779, 0.455674474707591, 0.481990908545298, 0.534589201601205, 0.560860688959535, 0.587076857978618, 0.60485210179211, 0.62055105523659, 0.644882012608307, 0.664734470125898, 0.679118961634057, 0.701878133478204, 0.721494103888148, 0.73157556985301, 0.75]

def test_SVC_V1():
    [x,y] = signals.SVC_V1(80)

    # assert x == test_x

def test_High_RA_V1():
    [x,y] = signals.High_RA_V1(80)

    # assert x == test_x

def test_High_RA_V2():
    [x,y] = signals.High_RA_V2(80)

    # assert x == test_x

def test_IVC_V1():
    [x,y] = signals.IVC_V1(80)

    # assert x == test_x

def test_IVC_V2():
    [x,y] = signals.IVC_V2(80)

    # assert x == test_x

def test_Mid_RA_V1():
    [x,y] = signals.Mid_RA_V1(80)

    # assert x == test_x

def test_Mid_RA_V2():
    [x,y] = signals.Mid_RA_V2(80)

    # assert x == test_x

def test_Low_RA_V1():
    [x,y] = signals.Low_RA_V1(80)

    # assert x == test_x

def test_Low_RA_V2():
    [x,y] = signals.Low_RA_V2(80)

    # assert x == test_x

def test_PA_V1():
    [x,y] = signals.PA_V1(80)

    # assert x == test_x

def test_PA_V2():
    [x,y] = signals.PA_V2(80)

    # assert x == test_x

def test_RV_V1():
    [x,y] = signals.RV_V1(80)

    # assert x == test_x

def test_RV_V2():
    [x,y] = signals.RV_V2(80)

    # assert x == test_x

def test_RV_Wall_V1():
    [x,y] = signals.RV_Wall_V1(80)

    # assert x == test_x

def test_RV_Wall_V2():
    [x,y] = signals.RV_Wall_V2(80)

    # assert x == test_x

def test_Default_Line():
    [x,y] = signals.Default_Line()
