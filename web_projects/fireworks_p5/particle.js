// this is the file that defines the Particle

function Particle(x, y, hue, exploder){
	// similar to C++ it has the constructors given below and some arguments

	this.pos = createVector(x,y);
	this.hue = hue;
	this.exploder = exploder;

	this.lifespan = 255; // how long the particle lasts

	if (exploder) {
		this.vel = createVector(random(-5, 5), random(-12, -5));
	} else {
		this.vel = p5.Vector.random2D();
		this.vel.mult(random(2, 10));
	}
	this.acc = createVector(0, 0);

	this.applyForce = function(force) {
		this.acc.add(force);
	}

	this.done = function() {
		if (this.lifespan < 0) {
			return true;
		} else {
			return false;
		}
	}

	this.update = function() {
		if (!this.exploder) {
			this.vel.mult(0.85);
			this.lifespan -= 4;
		}
		this.vel.add(this.acc);
		this.pos.add(this.vel);
		this.acc.mult(0);
	}

	this.show = function() {
		colorMode(HSB);
		if (!this.exploder){
			strokeWeight(2);
			stroke(this.hue, 255, 255, this.lifespan);
		} else {
			strokeWeight(4);
			stroke(this.hue, 255, 255);
		}
		point(this.pos.x, this.pos.y);
	}
}