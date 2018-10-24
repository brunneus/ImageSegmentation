using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using static DiseaseMeasurement.FormUpload;

namespace DiseaseMeasurement
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private Point? selectionAreaStart = null;
        private Mode currentMode;

        public MainWindow()
        {
            InitializeComponent();
            DataContext = new MainWindowDataContext();
        }

        private void load_image_button_click(object sender, RoutedEventArgs e)
        {
            var dialog = new OpenFileDialog();
            dialog.Filter = "Imagens |*.jpg;*.jpeg;*.png;...";

            if (dialog.ShowDialog().Value)
            {
                var dataContext = this.DataContext as MainWindowDataContext;
                dataContext.Image = new BitmapImage(new Uri(dialog.FileName));
                Reset();                
                currentMode = Mode.SelectingP1;
                UpdateInstructionsText();
            }
        }

        private void Image_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            var dataContext = this.DataContext as MainWindowDataContext;

            if (currentMode == Mode.SelectingP1)
            {
                dataContext.MeasureFirstpoint = e.GetPosition(canvas1);
                dataContext.MeasureSecondPoint = e.GetPosition(canvas1);
                currentMode = Mode.SelectingP2;
            }
            else if (currentMode == Mode.SelectingP2)
            {
                currentMode = Mode.SelectingArea;
            }
            else if (currentMode >= Mode.SelectingArea)
            {
                selectionAreaStart = e.GetPosition(canvas1);
                currentMode = Mode.CreatingSelection;                
            }

            this.UpdateInstructionsText();
        }

        private async void calculate_button_click(object sender, RoutedEventArgs e)
        {
            var dataContext = DataContext as MainWindowDataContext;

            dataContext.Text = "Analisado imagem, aguarde...";

            calculateBnt.IsEnabled = false;
            loadBnt.IsEnabled = false;
            resetBnt.IsEnabled = false;
            imageBox.IsEnabled = false;
            progressBar.Visibility = Visibility.Visible;

            var p1 = ConvertPicturePointToRealImagePoint(ConvertCanvasPointToPicturePoint(dataContext.MeasureFirstpoint));
            var p2 = ConvertPicturePointToRealImagePoint(ConvertCanvasPointToPicturePoint(dataContext.MeasureSecondPoint));

            var imageBytes = ImageUtils.BitmapImageToByteArray(dataContext.Image);
            var imageFile = new FileParameter(imageBytes);
            var pixelSize = Math.Abs(1d / (p2.Y - p1.Y));
            var selectionRect = BuildSelectionAreaRectangle();

            var @params = new Dictionary<string, object>
            {
                { "file", imageFile },
                { "pixel_size", pixelSize },
                { "x", selectionRect.X },
                { "y", selectionRect.Y },
                { "w", selectionRect.Width },
                { "h", selectionRect.Height },
            };

            var response = await MultipartFormDataPost("http://localhost:5000", "app", @params);

            var percentageAffected = response.Headers["percentage_affected"];
            var totalAreaAffected = response.Headers["total_area_affected"];

            var t = new BitmapImage();
            t.BeginInit();
            t.StreamSource = response.GetResponseStream();
            t.CacheOption = BitmapCacheOption.OnLoad;
            t.EndInit();

            var windowResultVM = new ResultWindowViewModel(t, percentageAffected, totalAreaAffected);
            var windowResult = new ResultsWindow { DataContext = windowResultVM };

            windowResult.Show();

            currentMode = Mode.SelectingArea;
            ResetSelectionArea();

            calculateBnt.IsEnabled = true;
            loadBnt.IsEnabled = true;
            resetBnt.IsEnabled = true;
            imageBox.IsEnabled = true;
            progressBar.Visibility = Visibility.Hidden;
            UpdateInstructionsText();
        }

        private void imageBox_MouseMove(object sender, MouseEventArgs e)
        {
            var dataContext = this.DataContext as MainWindowDataContext;

            if (currentMode == Mode.SelectingP2)
            {
                dataContext.MeasureSecondPoint = e.GetPosition(canvas1);
            }

            if (currentMode == Mode.CreatingSelection && e.LeftButton == MouseButtonState.Pressed)
            {
                var point = this.selectionAreaStart.Value;
                var mousePosition = e.GetPosition(canvas1);

                var top = Math.Min(mousePosition.Y, point.Y);
                var left = Math.Min(mousePosition.X, point.X);
                var width = Math.Abs(mousePosition.X - point.X);
                var height = Math.Abs(mousePosition.Y - point.Y);

                dataContext.SelectionAreaLeftOffset = left;
                dataContext.SelectionAreaTopOffset = top;
                dataContext.SelectionAreaWidth = width;
                dataContext.SelectionAreaHeight = height;

                Console.WriteLine(top);
                Console.WriteLine(left);
                Console.WriteLine(width);
                Console.WriteLine(height);
            }
        }

        private void imageBox_MouseWheel(object sender, MouseWheelEventArgs e)
        {
            var st = (MatrixTransform)this.imageBox.RenderTransform;
            double zoom = e.Delta > 0 ? .1 : -.1;
            var scale = e.Delta >= 0 ? 1.1 : (1.0 / 1.1); // choose appropriate scaling factor
            var position = e.GetPosition(imageBox);

            var matrix = st.Matrix;

            matrix.ScaleAtPrepend(scale, scale, position.X, position.Y);

            imageBox.RenderTransform = new MatrixTransform(matrix);
        }

        private void reset_Button_Click(object sender, RoutedEventArgs e)
        {
            this.Reset();
        }

        private void Reset()
        {
            var dataContext = this.DataContext as MainWindowDataContext;

            dataContext.MeasureFirstpoint = new Point(0, 0);
            dataContext.MeasureSecondPoint = new Point(0, 0);

            selectionAreaStart = null;

            currentMode = Mode.SelectingP1;
        }

        private void UpdateInstructionsText()
        {
            var dataContext = this.DataContext as MainWindowDataContext;

            if(currentMode == Mode.SelectingP1 | currentMode == Mode.SelectingP2)
            {
                dataContext.Text = "Selecione dois pontos onde a distância entre eles seja de 1cm.";
            }

            if(currentMode >= Mode.SelectingArea)
            {
                dataContext.Text = "Selecione a área da imagem na qual deseja realizar a análise.";
            }
        }

        private void ResetSelectionArea()
        {
            var dataContext = DataContext as MainWindowDataContext;
            dataContext.SelectionAreaLeftOffset = 0;
            dataContext.SelectionAreaTopOffset = 0;
            dataContext.SelectionAreaWidth = 0;
            dataContext.SelectionAreaHeight = 0;
        }

        private Int32Rect BuildSelectionAreaRectangle()
        {
            var dataContext = this.DataContext as MainWindowDataContext;

            var recCanvasStart = new Point(dataContext.SelectionAreaLeftOffset, dataContext.SelectionAreaTopOffset);
            var recCanvasEnd = new Point
            {
                X = dataContext.SelectionAreaLeftOffset + dataContext.SelectionAreaWidth,
                Y = dataContext.SelectionAreaTopOffset + dataContext.SelectionAreaHeight
            };

            var recImageStart = ConvertCanvasPointToPicturePoint(recCanvasStart);
            var recImageEnd = ConvertCanvasPointToPicturePoint(recCanvasEnd);

            var recRealImageStart = ConvertPicturePointToRealImagePoint(recImageStart);
            var recRealImageEnd = ConvertPicturePointToRealImagePoint(recImageEnd);

            return new Int32Rect
            {
                X = (int)recRealImageStart.X,
                Y = (int)recRealImageStart.Y,
                Width = (int)(recRealImageEnd.X - recRealImageStart.X),
                Height = (int)(recRealImageEnd.Y - recRealImageStart.Y)
            };
        }

        private Point ConvertCanvasPointToPicturePoint(Point canvasPoint)
        {
            var posPic = new Point
            {
                X = canvasPoint.X - ((canvas1.ActualWidth / 2) - (imageBox.ActualWidth / 2)),
                Y = canvasPoint.Y - ((canvas1.ActualHeight / 2) - (imageBox.ActualHeight / 2))
            };

            return posPic;
        }

        private Point ConvertPicturePointToRealImagePoint(Point point)
        {
            var dataContext = DataContext as MainWindowDataContext;

            var leftPercentage = point.X / imageBox.ActualWidth;
            var topPercentage = point.Y / imageBox.ActualHeight;

            var x = dataContext.Image.PixelWidth * leftPercentage;
            var y = dataContext.Image.PixelHeight * topPercentage;

            return new Point(x, y);
        }
    }

    public enum Mode
    {
        None,
        SelectingP1,
        SelectingP2,
        SelectingArea,
        CreatingSelection
    }
}
