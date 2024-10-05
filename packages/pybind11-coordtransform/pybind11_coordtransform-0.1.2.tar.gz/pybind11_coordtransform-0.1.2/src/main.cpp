#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

#include <Eigen/Dense>
#include <cmath>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;
using namespace pybind11::literals;

constexpr double x_PI = 3.14159265358979324 * 3000.0 / 180.0;
constexpr double PI = 3.1415926535897932384626; // M_PI
constexpr double a = 6378245.0;
constexpr double ee = 0.00669342162296594323;

inline double transformlng(double lng, double lat)
{
    // clang-format off
    double ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * std::sqrt(std::fabs(lng));
    ret += (20.0 * std::sin(6.0 * lng * PI) + 20.0 * std::sin(2.0 * lng * PI)) * 2.0 / 3.0;
    ret += (20.0 * std::sin(lng * PI) + 40.0 * std::sin(lng / 3.0 * PI)) * 2.0 / 3.0;
    ret += (150.0 * std::sin(lng / 12.0 * PI) + 300.0 * std::sin(lng / 30.0 * PI)) * 2.0 / 3.0;
    // clang-format on
    return ret;
}

inline double transformlat(double lng, double lat)
{
    // clang-format off
    double ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * std::sqrt(std::fabs(lng));
    ret += (20.0 * std::sin(6.0 * lng * PI) + 20.0 * std::sin(2.0 * lng * PI)) * 2.0 / 3.0;
    ret += (20.0 * std::sin(lat * PI) + 40.0 * std::sin(lat / 3.0 * PI)) * 2.0 / 3.0;
    ret += (160.0 * std::sin(lat / 12.0 * PI) + 320 * std::sin(lat * PI / 30.0)) * 2.0 / 3.0;
    // clang-format on
    return ret;
}

inline bool out_of_china(double lng, double lat)
{
    return !(73.66 < lng && lng < 135.05 && 3.86 < lat && lat < 53.55);
}

inline Eigen::Vector2d bd09togcj02(double bd_lng, double bd_lat)
{
    double x = bd_lng - 0.0065;
    double y = bd_lat - 0.006;
    double z = std::sqrt(x * x + y * y) - 0.00002 * std::sin(y * x_PI);
    double theta = std::atan2(y, x) - 0.000003 * std::cos(x * x_PI);
    double gg_lng = z * std::cos(theta);
    double gg_lat = z * std::sin(theta);
    return {gg_lng, gg_lat};
}

inline Eigen::Vector2d gcj02tobd09(double lng, double lat)
{
    double z =
        std::sqrt(lng * lng + lat * lat) + 0.00002 * std::sin(lat * x_PI);
    double theta = std::atan2(lat, lng) + 0.000003 * std::cos(lng * x_PI);
    double bd_lng = z * std::cos(theta) + 0.0065;
    double bd_lat = z * std::sin(theta) + 0.006;
    return {bd_lng, bd_lat};
}

inline Eigen::Vector2d wgs84togcj02(double lng, double lat,
                                    bool check_output_china = true)
{
    if (check_output_china && out_of_china(lng, lat)) {
        return {lng, lat};
    }
    double dlat = transformlat(lng - 105.0, lat - 35.0);
    double dlng = transformlng(lng - 105.0, lat - 35.0);
    double radlat = lat / 180.0 * PI;
    double magic = std::sin(radlat);
    magic = 1.0 - ee * magic * magic;
    double sqrtmagic = std::sqrt(magic);
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI);
    dlng = (dlng * 180.0) / (a / sqrtmagic * std::cos(radlat) * PI);
    double mglat = lat + dlat;
    double mglng = lng + dlng;
    return {mglng, mglat};
}

inline Eigen::Vector2d gcj02towgs84(double lng, double lat,
                                    bool check_output_china = true)
{
    if (check_output_china && out_of_china(lng, lat)) {
        return {lng, lat};
    }
    double dlat = transformlat(lng - 105.0, lat - 35.0);
    double dlng = transformlng(lng - 105.0, lat - 35.0);
    double radlat = lat / 180.0 * PI;
    double magic = std::sin(radlat);
    magic = 1 - ee * magic * magic;
    double sqrtmagic = std::sqrt(magic);
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI);
    dlng = (dlng * 180.0) / (a / sqrtmagic * std::cos(radlat) * PI);
    double mglat = lat + dlat;
    double mglng = lng + dlng;
    return {lng * 2 - mglng, lat * 2 - mglat};
}

PYBIND11_MODULE(_core, m)
{
    m.doc() = R"pbdoc(
        c++/python version of https://github.com/wandergis/coordtransform
    )pbdoc";

    m.def("bd09togcj02", &bd09togcj02, "lng"_a, "lat"_a,
          R"pbdoc(
          Convert BD09 coordinates to GCJ02 coordinates.

          Args:
              lng (float): Longitude in BD09 coordinate system.
              lat (float): Latitude in BD09 coordinate system.

          Returns:
              tuple: A tuple containing (longitude, latitude) in GCJ02 coordinate system.
          )pbdoc");

    m.def("gcj02tobd09", &gcj02tobd09, "lng"_a, "lat"_a,
          R"pbdoc(
          Convert GCJ02 coordinates to BD09 coordinates.

          Args:
              lng (float): Longitude in GCJ02 coordinate system.
              lat (float): Latitude in GCJ02 coordinate system.

          Returns:
              tuple: A tuple containing (longitude, latitude) in BD09 coordinate system.
          )pbdoc");

    m.def("wgs84togcj02", &wgs84togcj02, "lng"_a, "lat"_a,
          "check_out_of_china"_a = true,
          R"pbdoc(
          Convert WGS84 coordinates to GCJ02 coordinates.

          Args:
              lng (float): Longitude in WGS84 coordinate system.
              lat (float): Latitude in WGS84 coordinate system.
              check_out_of_china (bool, optional): If True, check if the coordinates are outside China. Defaults to True.

          Returns:
              tuple: A tuple containing (longitude, latitude) in GCJ02 coordinate system.
          )pbdoc");

    m.def("gcj02towgs84", &gcj02towgs84, "lng"_a, "lat"_a,
          "check_out_of_china"_a = true,
          R"pbdoc(
          Convert GCJ02 coordinates to WGS84 coordinates.

          Args:
              lng (float): Longitude in GCJ02 coordinate system.
              lat (float): Latitude in GCJ02 coordinate system.
              check_out_of_china (bool, optional): If True, check if the coordinates are outside China. Defaults to True.

          Returns:
              tuple: A tuple containing (longitude, latitude) in WGS84 coordinate system.
          )pbdoc");

    m.def("out_of_china", &out_of_china, "lng"_a, "lat"_a,
          R"pbdoc(
          Check if the given coordinates are outside China.

          Args:
              lng (float): Longitude.
              lat (float): Latitude.

          Returns:
              bool: True if the coordinates are outside China, False otherwise.
          )pbdoc");

    using RowVectorsNx3 =
        Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor>;
    using RowVectorsNx2 =
        Eigen::Matrix<double, Eigen::Dynamic, 2, Eigen::RowMajor>;

    m.def(
        "wgs84_to_gcj02_Nx3",
        [](const RowVectorsNx3 &coords, bool check_out_of_china) {
            const size_t N = coords.rows();
            if (!N) {
                return coords;
            }
            if (check_out_of_china &&
                out_of_china(coords(0, 0), coords(0, 1))) {
                return coords;
            }
            RowVectorsNx3 converted = coords;
            for (size_t i = 0; i < N; ++i) {
                auto xy = wgs84togcj02(coords(i, 0), coords(i, 1), false);
                converted(i, 0) = xy[0];
                converted(i, 1) = xy[1];
            }
            return converted;
        },
        "coords"_a, "check_out_of_china"_a = true,
        R"pbdoc(
        Convert multiple WGS84 coordinates to GCJ02 coordinates (for Nx3 matrices).

        Args:
            coords (numpy.ndarray): Nx3 array of coordinates in WGS84 system.
            check_out_of_china (bool, optional): If True, check if the first coordinate is outside China. Defaults to True.

        Returns:
            numpy.ndarray: Nx3 array of coordinates in GCJ02 system.
        )pbdoc");

    m.def(
        "wgs84_to_gcj02_Nx2",
        [](const RowVectorsNx2 &coords, bool check_out_of_china) {
            const size_t N = coords.rows();
            if (!N) {
                return coords;
            }
            if (check_out_of_china &&
                out_of_china(coords(0, 0), coords(0, 1))) {
                return coords;
            }
            RowVectorsNx2 converted = coords;
            for (size_t i = 0; i < N; ++i) {
                auto xy = wgs84togcj02(coords(i, 0), coords(i, 1), false);
                converted(i, 0) = xy[0];
                converted(i, 1) = xy[1];
            }
            return converted;
        },
        "coords"_a, "check_out_of_china"_a = true,
        R"pbdoc(
        Convert multiple WGS84 coordinates to GCJ02 coordinates (for Nx2 matrices).

        Args:
            coords (numpy.ndarray): Nx2 array of coordinates in WGS84 system.
            check_out_of_china (bool, optional): If True, check if the first coordinate is outside China. Defaults to True.

        Returns:
            numpy.ndarray: Nx2 array of coordinates in GCJ02 system.
        )pbdoc");

    m.def(
        "gcj02_to_wgs84_Nx3",
        [](const RowVectorsNx3 &coords, bool check_out_of_china) {
            const size_t N = coords.rows();
            if (!N) {
                return coords;
            }
            if (check_out_of_china &&
                out_of_china(coords(0, 0), coords(0, 1))) {
                return coords;
            }
            RowVectorsNx3 converted = coords;
            for (size_t i = 0; i < N; ++i) {
                auto xy = gcj02towgs84(coords(i, 0), coords(i, 1), false);
                converted(i, 0) = xy[0];
                converted(i, 1) = xy[1];
            }
            return converted;
        },
        "coords"_a, "check_out_of_china"_a = true,
        R"pbdoc(
        Convert multiple GCJ02 coordinates to WGS84 coordinates (for Nx3 matrices).

        Args:
            coords (numpy.ndarray): Nx3 array of coordinates in GCJ02 system.
            check_out_of_china (bool, optional): If True, check if the first coordinate is outside China. Defaults to True.

        Returns:
            numpy.ndarray: Nx3 array of coordinates in WGS84 system.
        )pbdoc");

    m.def(
        "gcj02_to_wgs84_Nx2",
        [](const RowVectorsNx2 &coords, bool check_out_of_china) {
            const size_t N = coords.rows();
            if (!N) {
                return coords;
            }
            if (check_out_of_china &&
                out_of_china(coords(0, 0), coords(0, 1))) {
                return coords;
            }
            RowVectorsNx2 converted = coords;
            for (size_t i = 0; i < N; ++i) {
                auto xy = gcj02towgs84(coords(i, 0), coords(i, 1), false);
                converted(i, 0) = xy[0];
                converted(i, 1) = xy[1];
            }
            return converted;
        },
        "coords"_a, "check_out_of_china"_a = true,
        R"pbdoc(
        Convert multiple GCJ02 coordinates to WGS84 coordinates (for Nx2 matrices).

        Args:
            coords (numpy.ndarray): Nx2 array of coordinates in GCJ02 system.
            check_out_of_china (bool, optional): If True, check if the first coordinate is outside China. Defaults to True.

        Returns:
            numpy.ndarray: Nx2 array of coordinates in WGS84 system.
        )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
