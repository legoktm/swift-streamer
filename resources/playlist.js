$(function(){
	console.log('ready');
	var queue, player, cover, config;
	config = JSON.parse($('#config').text());

	queue = {
		'_queue': [],
		'add': function(input) {
			this._queue.push(input);
			console.log('Adding ' + input.name + ' to the queue.');
			$('#queue').append(
				$('<li class="in-queue">').text(
					input.name + ' - ' + input.album
				)
			);
			player.start();
		},
		'pop': function() {
			return this._queue.shift();
		},
		'hasMore': function() {
			return this._queue.length !== 0;
		}
	};

	cover = {
		'switch': function(album) {
			$('#cover').attr({
				'src': 'covers/' + album + '.jpg'
			});
		},
		'hide': function() {
			$('#cover').attr('src', '');
		}
	};

	player = {
		'playing': false,
		'start': function() {
			if (!this.playing) {
				this.playing = true;
				this.play();
			}
		},
		'play': function() {
			var $player = $('#player'),
				song = queue.pop();
			console.log('Starting to play: ' + song.src);
			$player.empty();
			$player.append($('<source>').attr({
				'src': song.src + '.mp3',
				'type': 'audio/mpeg'
			}));
			if (config.ogg) {
				$player.append($('<source>').attr({
					'src': song.src + '.ogg',
					'type': 'audio/ogg'
				}));
			}
			$player[0].load();
			$player[0].play();
			cover.switch(song.hash_);
		},
		'next': function() {
			if (queue.hasMore()) {
				this.play();
			} else {
				this.playing = false;
				cover.hide();
			}
		}
	};

	$('#player').on('ended', function(e){
		// Remove the one that just ended
		console.log('Finished, moving to next track, maybe.');
		$('.in-queue').first().remove();
		player.next();
	});

	$('.add-queue').click(function(e) {
		var $this = $(this);
		console.log('click');
		e.preventDefault();
		queue.add({
			'src': $this.data('src'),
			'name': $this.text(),
			'album': $this.data('album'),
			'hash_': $this.data('hash')
		});
	});

	$('.play-album').click(function() {
		$(this).next('ol').find('.add-queue').click();
	});
});
