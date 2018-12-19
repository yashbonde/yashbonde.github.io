const deckgl = new deck.DeckGL({
		container: 'container',
		longitude: -122.45,
		latitude: 37.8,
		zoom: 12,
		layers: [
			new deck.ScatterplotLayer({
				data: [
					{position: [-122.45, 37.8], color: [255, 0, 0], radius: 1000}
				]
			}),
			new deck.TextLayer({
				data: [
					{position: [-122.45, 37.8], text: 'Hello World'}
				]
			})
		]
	});