Example Usage of PiTweener
==========================

::

    import PiTweener
    
    tweener = PiTweener.Tweener()
    # add a tween:
    tweener.add_tween(
        my_rocket,
        throttle = 50,
        set_thrust = 400,
        tween_time = 5.0,
        tween_type = tweener.OUT_QUAD,
        on_complete_function = my_rocket.burn
    )
    
    # get a tween and modify it:
    mt = tweener.get_tweens_affecting_object(my_rocket)[0]
    tweenable = mt.get_tweenable("throttle")
    tweener.add_tween(tweenable, change=1000, tween_time=0.7)
    tweener.add_tween(mt, duration=-0.2, tween_time=0.2)


Unit Tests
----------

Unit tests can be executed simply by running PiTweenerTest::

    python PiTweenerTest.py

