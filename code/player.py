import pygame 
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/player/personagem1.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = pygame.Rect(self.rect.left - 20, self.rect.bottom, self.rect.width - 20, 20)

		# graphics setup
		self.import_player_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15

		# movement 
		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None

		self.obstacle_sprites = obstacle_sprites

	def import_player_assets(self):
		character_path = '../graphics/player/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			# movement input
			if keys[MOVE_UP] or keys[MOVE_UP1]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[MOVE_DOWN] or keys[MOVE_DOWN1]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[MOVE_RIGHT] or keys[MOVE_RIGHT1]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[MOVE_LEFT] or keys[MOVE_LEFT1]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			# attack input
			if keys[ATTACK] or keys[ATTACK1]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				print('attack')

			# magic input
			#if keys[MAGIC] or keys[MAGIC1]:
			#	self.attacking = True
			#	self.attack_time = pygame.time.get_ticks()
			#	print('magic')

	def get_status(self):

		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()
		keys = pygame.key.get_pressed()
		if keys[SPRINT] or keys[SPRINT1]:
			speed = speed*1.8
		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def take_damage(self, amount):
		self.health -= amount
		if self.health <= 0:
			self.die()

	def die(self):
		# Lógica de morte do jogador
		print("Player died!")

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)
