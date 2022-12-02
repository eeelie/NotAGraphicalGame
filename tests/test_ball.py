from ball import Ball
from pytest import approx

def test_time_step():
	ball =  Ball(1,0.5,0,0,1,0)
	ball.p, ball.v = ball.time_step(1)
	assert ball.p == approx([0.95, -0.05])
	assert ball.v == approx([0.9,-0.1])

def test_collides_with():
	B1 = Ball(1,0.5,0,0,0,0)
	B2 = Ball(2,0.5,1,0,0,0)
	B3 = Ball(3,0.5,0.3,0.95,0,0)
	B4 = Ball(4,0.5,3,1,0,0)

	assert B1.collides_with(B2) == True
	assert B1.collides_with(B3) == True
	assert B1.collides_with(B4) == False

	assert B2.collides_with(B1) == True
	assert B2.collides_with(B3) == False
	assert B2.collides_with(B4) == False

	assert B3.collides_with(B1) == True
	assert B3.collides_with(B2) == False
	assert B3.collides_with(B4) == False

	assert B4.collides_with(B1) == False
	assert B4.collides_with(B2) == False
	assert B4.collides_with(B3) == False

def test_collides_with_table():
	B1 = Ball(1,0.025,-0.5,1.2,0,0)
	B2 = Ball(2,0.025,0.61,0.9,0,0)
	B3 = Ball(3,0.025,-0.5,-1.3,0,0)
	
	assert B1.collides_with_table(1.27,2.54) == False
	assert B2.collides_with_table(1.27,2.54) == True
	assert B3.collides_with_table(1.27,2.54) == True
