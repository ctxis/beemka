<?php
// Change these settings if you need to.
$storage = '/tmp/beemka-image';
$paramName = 'data';

// Don't change anything below this line.
$storage = rtrim($storage, "\\/") . DIRECTORY_SEPARATOR;

class ImageStorage {
    protected $storage = '';

    public function __construct($storage)
    {
        $this->storage = $storage;
        $this->setup();
    }

    protected function setup()
    {
        if (!is_dir($this->storage)) {
            mkdir($this->storage, 0777, true);
            if (!is_dir($this->storage)) {
                throw new Exception('Could not create storage path: ' . $this->storage);
            }
        } elseif (!is_writable($this->storage)) {
            throw new Exception($this->storage . ' is not writable');
        }
    }

    protected function getCurrentFiles()
    {
        $storage = $this->storage;
        $allFiles = array_map(
            function ($file) use ($storage) {
                $file = str_ireplace('.png', '', $file);
                return substr($file, strlen($storage));
            },
            glob($this->storage . "*.png")
        );
        rsort($allFiles);
        return $allFiles;
    }

    protected function getLastImage()
    {
        $allFiles = $this->getCurrentFiles();
        return (count($allFiles) == 0) ? '' : $allFiles[0] . '.png';
    }

    protected function getNextImage()
    {
        $allFiles = $this->getCurrentFiles();
        $fileName = (count($allFiles) == 0) ? 1 : ++$allFiles[0];
        return $fileName . '.png';
    }

    protected function serveImage($filePath)
    {
        header("Content-Type: image/png");
        header('Expires: 0');
        header("Content-Length: " . filesize($filePath));
        readfile($filePath);
        die();
    }

    public function serveLastImage()
    {
        $image = $this->getLastImage();
        $fullPath = $this->storage . $image;
        $this->serveImage($fullPath);
    }

    public function saveImage($data)
    {
        $saveAs = $this->getNextImage();
        $data = trim(str_replace('data:image/png;base64,', '', $data));
        file_put_contents($this->storage . $saveAs, base64_decode($data));
    }
}

$imageStorage = new ImageStorage($storage);

if (isset($_GET['image'])) {
    $imageStorage->serveLastImage();
    die();
}

$data = isset($_REQUEST[$paramName]) ? trim($_REQUEST[$paramName]) : '';
if (!empty($data)) {
    $imageStorage->saveImage($data);
    die();
}

?>
<html>
<head>
    <title>Beemka Image Viewer</title>
</head>
<body>
    <img id="viewer" src="#" width="100%">

    <script type="text/javascript">
        setInterval(
            function() {
                let viewer = document.getElementById('viewer');
                viewer.setAttribute('src', '<?php echo basename(__FILE__); ?>?image&_=' + Date.now());
            },
            1000
        );
    </script>
</body>
</html>
