using System;
using System.Windows.Media.Imaging;

namespace DiseaseMeasurement
{
    public class ResultWindowViewModel
    {
        public ResultWindowViewModel(BitmapImage imageResult, string percentageAffected, string areaAffected)
        {
            ImageResult = imageResult;

            var percentageAsNumber = double.Parse(percentageAffected);
            var areaAsNumber = double.Parse(areaAffected);

            PercentageText = $"{Math.Round(percentageAsNumber, 2)}% da folha está infectada";
            AreaText = $"{Math.Round(areaAsNumber, 2)}mm de área infectada";
        }

        public BitmapImage ImageResult { get; set; }
        public string PercentageText { get; set; }
        public string AreaText { get; set; }
    }
}
