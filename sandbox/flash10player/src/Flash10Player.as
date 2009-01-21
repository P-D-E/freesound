package  {    import flash.ui.Keyboard;        import ui.IButton;    import ui.IButtonObserver;    import ui.ISoundDisplayObserver;    import ui.ImageButton;    import ui.SoundDisplay;    import flash.display.Sprite;    import flash.events.KeyboardEvent;    import flash.events.MouseEvent;            [SWF( backgroundColor='0xffffff', width='900', height='149', frameRate='60')]    public class Flash10Player extends Sprite implements ISoundManagerObserver, IButtonObserver, ISoundDisplayObserver    {        private var _soundDisplay : SoundDisplay;        private var _baseUrl : String, _waveformUrl : String, _spectralUrl : String, _soundUrl : String;        private var _durationEstimate : Number;        private var _sound : BasicSoundManager;        [Embed(source='../media/play.png')]        private var PlayButtonImage : Class;        private var playButton : ImageButton;        [Embed(source='../media/stop.png')]        private var StopButtonImage : Class;        private var stopButton : ImageButton;        [Embed(source='../media/spectral.png')]        private var SpectralButtonImage : Class;        private var spectralButton : ImageButton;        [Embed(source='../media/loop.png')]        private var LoopButtonImage : Class;        private var loopButton : ImageButton;        private var _hidingSprite : Sprite;        public function Flash10Player()        {            if (loaderInfo.parameters.baseUrl)	            _baseUrl = loaderInfo.parameters.baseUrl;            else            	_baseUrl = "../media/";            	            if (loaderInfo.parameters.waveformUrl)	            _waveformUrl = loaderInfo.parameters.waveformUrl;            else            	_waveformUrl = "waveform.png";            if (loaderInfo.parameters.spectralUrl)	            _spectralUrl = loaderInfo.parameters.spectralUrl;            else            	_spectralUrl = "spectral.jpg";                        if (loaderInfo.parameters.soundUrl)            	_soundUrl = loaderInfo.parameters.soundUrl;            else	            _soundUrl = "preview.mp3";	                        if (loaderInfo.parameters.duration)            	_durationEstimate = loaderInfo.parameters.duration;            else	            _durationEstimate = 3457.95;            buildUi();        }        private function createSoundManager():void        {            if (!_sound)            {                _sound = new BasicSoundManager(_baseUrl + _soundUrl);                _sound.addSoundManagerObserver(this);            }        }        public function onSoundDisplayClick(soundDisplay : SoundDisplay, procent : Number) : void        {        	createSoundManager();            _sound.jump(procent);        }        public function onButtonDown(button : IButton) : void        {            switch (button)            {                case playButton:                    {		        	createSoundManager();                    _sound.play();                    break;                    }                case stopButton:                    {                    if (_sound)		        			_sound.stop();                    break;                    }                case spectralButton:                    {		        		_soundDisplay.setSpectralBackground();		        		break;		        	}		        case loopButton:			        {			        	if (_sound)			        		_sound.loop = true;			        	break;			        }            }        }                public function onButtonUp(button:IButton):void        {            switch (button)            {                case playButton:                    {		        		if (_sound)		                	_sound.pause();	                    break;	        		}		        case spectralButton:		        	{		        		_soundDisplay.setWaveformBackground();		        		break;		        	}		        case loopButton:			        {			        	if (_sound)			        		_sound.loop = false;			        	break;			        }            }        }        private function buildUi() : void        {            _soundDisplay = new SoundDisplay(900, 149, _baseUrl + _waveformUrl, _baseUrl + _spectralUrl, _durationEstimate);            _soundDisplay.addSoundDisplayObserver(this);            addChild(_soundDisplay);                        var padding:int = 3;            playButton = new ImageButton(new PlayButtonImage(), true);            playButton.addButtonObserver(this);            playButton.x = 0;            playButton.y = 149 - 40;            _soundDisplay.addChild(playButton);                        _hidingSprite = new Sprite();        	            stopButton = new ImageButton(new StopButtonImage());            stopButton.addButtonObserver(this);            stopButton.x = playButton.x + playButton.width + padding;            stopButton.y = 149 - 40;            _hidingSprite.addChild(stopButton);            spectralButton = new ImageButton(new SpectralButtonImage(), true);            spectralButton.addButtonObserver(this);            spectralButton.x = stopButton.x + stopButton.width + padding;            spectralButton.y = 149 - 40;            _hidingSprite.addChild(spectralButton);            loopButton = new ImageButton(new LoopButtonImage(), true);            loopButton.addButtonObserver(this);            loopButton.x = spectralButton.x + spectralButton.width + padding;            loopButton.y = 149 - 40;            _hidingSprite.addChild(loopButton);                        _hidingSprite.y = 50;                        _soundDisplay.addChild(_hidingSprite);            _soundDisplay.addEventListener(MouseEvent.MOUSE_OVER, onMouseOver);            _soundDisplay.addEventListener(MouseEvent.MOUSE_OUT, onMouseOut);        }                private function onMouseOver(e:MouseEvent):void        {            _hidingSprite.y = 0;        }        private function onMouseOut(e:MouseEvent):void        {            _hidingSprite.y = 50;        }        public function onSoundManagerLoading( soundManager : ISoundManager, progress : Number ) : void        {            _soundDisplay.setSoundDuration(_sound.duration);            _soundDisplay.setLoading(progress);        };        public function onSoundManagerError( soundManager : ISoundManager, errorMsg : String ) : void        {        	// TODO: gracefully display fail message. Epic fail!        };        public function onSoundManagerLoaded(soundManager : ISoundManager) : void        {            _soundDisplay.setSoundDuration(_sound.duration);            _soundDisplay.setLoading(1.0);        };        public function onSoundManagerPlay(soundManager : ISoundManager) : void        {            playButton.setState(true);        };        public function onSoundManagerPlaying( soundManager : ISoundManager, position : Number, time: Number ) : void        {            _soundDisplay.setPlaying(position, time);        };        public function onSoundManagerPause(soundManager : ISoundManager) : void        {            playButton.setState(false);        };        public function onSoundManagerStop(soundManager : ISoundManager) : void        {            playButton.setState(false);        };    }}