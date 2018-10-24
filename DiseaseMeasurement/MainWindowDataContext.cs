using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace DiseaseMeasurement
{
    public class MainWindowDataContext : INotifyPropertyChanged
    {
        public MainWindowDataContext()
        {
        }

        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
        }

        public event PropertyChangedEventHandler PropertyChanged = delegate { };

        private string _text = "Carregue uma imagem para iniciar a análise";
        public string Text
        {
            get { return _text; }
            set
            {
                _text = value;
                OnPropertyChanged(nameof(Text));
            }
        }
        
        private BitmapImage _image;
        public BitmapImage Image
        {
            get { return _image; }
            set
            {
                _image = value;
                PropertyChanged(this, new PropertyChangedEventArgs("Image"));
            }
        }

        private Point _measureFirstPoint;
        public Point MeasureFirstpoint
        {
            get { return _measureFirstPoint; }
            set
            {
                _measureFirstPoint = value;
                this.OnPropertyChanged("MeasureFirstpoint");
            }
        }

        private Point _measureSecondPoint;
        public Point MeasureSecondPoint
        {
            get { return _measureSecondPoint; }
            set
            {
                _measureSecondPoint = value;
                this.OnPropertyChanged("MeasureSecondPoint");
            }
        }

        private double _selectionAreaLeftOffset;
        public double SelectionAreaLeftOffset
        {
            get { return _selectionAreaLeftOffset; }
            set
            {
                _selectionAreaLeftOffset = value;
                PropertyChanged(this, new PropertyChangedEventArgs("SelectionAreaLeftOffset"));
            }
        }

        private double _selectionAreaTopOffset;
        public double SelectionAreaTopOffset
        {
            get { return _selectionAreaTopOffset; }
            set
            {
                _selectionAreaTopOffset = value;
                PropertyChanged(this, new PropertyChangedEventArgs("SelectionAreaTopOffset"));
            }
        }

        private double _selectionAreaWidth;
        public double SelectionAreaWidth
        {
            get { return _selectionAreaWidth; }
            set
            {
                _selectionAreaWidth = value;
                PropertyChanged(this, new PropertyChangedEventArgs("SelectionAreaWidth"));
            }
        }

        private double _selectionAreaHeight;
        public double SelectionAreaHeight
        {
            get { return _selectionAreaHeight; }
            set
            {
                _selectionAreaHeight = value;
                PropertyChanged(this, new PropertyChangedEventArgs("SelectionAreaHeight"));
            }
        }
    }
}
