function Firework() {
	this.firework = new Particle(random(width), height, this.hue, true);
	this.exploded = false;
	this.blown_particles = [];

	this.hue = random(255);

	this.update = function() {
		if (!this.exploded) {
			// update the firework only if it exists
			this.firework.applyForce(gravity);
			this.firework.update();

			// how to check if the firework is at top
			if (this.firework.vel.y >= 0) {
				this.exploded = true;

				this.explode_particle();
			}
		}
		
		// we want the particles to experience the physics as well
		for (var i = this.blown_particles.length - 1; i >= 0; i--) {
			this.blown_particles[i].applyForce(gravity);
			this.blown_particles[i].update();

			if (this.blown_particles[i].done()) {
				// splice is a JS function that deletes something from an array
				this.blown_particles.splice(i, 1);
			}
		}
	}

	this.done = function() {
		if (this.exploded && this.blown_particles.length == 0) {
			return true;
		} else {
			return false;
		}
	}

	this.explode_particle = function() {
		// we need to make a make many particles here
		for (var i = 0; i < random(20, 100); i++) {
			var p = new Particle(this.firework.pos.x, this.firework.pos.y, this.hue, false);
			this.blown_particles.push(p);
		}
	}

	this.show = function() {
		 
		if (!this.exploded) {
			// show only if it exists
			this.firework.show();
		}

		for (var i = 0; i < this.blown_particles.length; i++) {
			this.blown_particles[i].show();
		}
	}
}