<?php
// Change these settings if you need to.
$storage = '/tmp/beemka-files';
$paramFile = 'file';
$paramData = 'data';

// Don't change anything below this line.
class FileStorage {
    protected $storage = '';
    protected $files = [];
    protected $indexFilename = 'index.txt';
    protected $indexFullPath = '';
    protected $indexSeparator = '[|]';

    public function __construct($storage)
    {
        $this->storage = $storage;
        $this->indexFullPath = $this->storage . $this->indexFilename;
        $this->setup();
        $this->loadIndex();
    }

    protected function loadIndex()
    {
        $this->files = [];
        if (!file_exists($this->indexFullPath)) {
            return true;
        }

        $list = array_filter(
            explode(PHP_EOL, file_get_contents($this->indexFullPath)),
            function ($f) {
                return !empty($f);
            }
        );

        foreach ($list as $item) {
            list($index, $path) = explode($this->indexSeparator, $item);
            $this->files[$index] = $path;
        }

        return true;
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

    public function saveFile($file, $data)
    {
        $newName = time() . '_' . md5(rand(1, 10000)) . '.txt';
        file_put_contents($this->storage . $newName, base64_decode($data));
        //file_put_contents($this->storage . $newName, $data);

        file_put_contents($this->indexFullPath, $newName . $this->indexSeparator . $file . PHP_EOL, FILE_APPEND);
        return true;
    }

    public function getFileData($file)
    {
        if (!isset($this->files[$file])) {
            return '';
        }
        return file_get_contents($this->storage . $file);
    }

    public function getContentsHTML()
    {
        $html = [];
        $html[] = '<ul>';
        foreach ($this->files as $index => $path) {
            $html[] = "<li><a href='./file.php?view={$index}'>{$path}</a></li>";
        }
        $html[] = '</ul>';

        return implode(PHP_EOL, $html);
    }
}

$storage = rtrim($storage, "\\/") . DIRECTORY_SEPARATOR;
$fileStorage = new FileStorage($storage);

$file = isset($_REQUEST[$paramFile]) ? trim($_REQUEST[$paramFile]) : '';
$data = isset($_REQUEST[$paramData]) ? trim($_REQUEST[$paramData]) : '';

if (!empty($file) && !empty($data)) {
    $fileStorage->saveFile($file, $data);
    die();
}

if (isset($_GET['index'])) {
    echo $fileStorage->getContentsHTML();
    die();
}

$view = isset($_GET['view']) ? trim($_GET['view']) : '';
$fileData = $fileStorage->getFileData($view);
?>
<html>
<head>
    <title>Beemka File Viewer</title>
</head>
<body>
    <table width="100%" border="0" cellpadding="4" cellspacing="4">
        <tr>
            <th width="0%">Files</th>
            <th width="100%">Contents</th>
        </tr>
        <tr>
            <td valign="top" nowrap="nowrap" id="contents">
                <?php echo $fileStorage->getContentsHTML(); ?>
            </td>
            <td valign="top">
            <pre><?php echo htmlspecialchars($fileData, ENT_QUOTES); ?></pre>
            </td>
        </tr>
    </table>

    <script type="text/javascript">
        setInterval(
            () => {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = () => {
                     if (xhttp.readyState == XMLHttpRequest.DONE) {
                        document.getElementById('contents').innerHTML = xhttp.responseText;
                     }
                }
                xhttp.open("GET", './file.php?index', true);
                xhttp.send();
            },
            5000
        );
    </script>
</body>
</html>
