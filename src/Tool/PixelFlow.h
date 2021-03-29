/**
 * @file PixelFlow.h
 * @author duyanwei (duyanwei0702@gmail.com)
 * @brief
 * @version 0.1
 * @date 2021-03-29
 *
 * @copyright Copyright (c) 2021
 *
 */

#ifndef DSO_PIXEL_FLOW_H_
#define DSO_PIXEL_FLOW_H_

#include <exception>

#include "util/NumType.h"

namespace dso
{
/**
 * @brief flow estimation
 *
 * @ref Robotics, Vision and Control, CH15.2, eq(15.6)
 */
class PixelFlow
{
public:
    /**
     * @brief compute camera velocity in reference frame
     *
     * @param tr timestamp of reference frame
     * @param Twr camera pose of reference frame in world frame
     * @param tf timestamp of frame
     * @param Twf camera pose of frame in world frame
     * @return Vec6
     */
    static Vec6 computeVelocity(const double tr, const SE3& Twr,
                                const double tf, const SE3& Twf)
    {
        const double dt = tf - tr;

        if (dt <= 0.0)
        {
            throw std::runtime_error(
                "invalid timestamp when computing camera velocity");
        }

        const SE3  Trf = Twr.inverse() * Twf;
        const Vec3 Vrf = Trf.translation() / dt;
        const Vec3 Wrf = Trf.so3().log() / dt;

        Vec6 velocity;
        velocity << Vrf, Wrf;
        return velocity;
    }

    /**
     * @brief
     */
    static Vec2 computeFlow(double u, double v, double idepth, double fx,
                            double fy, double cx, double cy,
                            const Vec6& velocity)
    {
        const Mat26 J = computeJacobian(u, v, idepth, fx, fy, cx, cy);
        return J * velocity;
    }

    /**
     * @brief compute image jacobian
     */
    static const Mat26 computeJacobian(double u, double v, double idepth,
                                       double fx, double fy, double cx,
                                       double cy)
    {
        const double uc   = u - cx;
        const double vc   = v - cy;
        const double ucvc = uc * vc;
        const double uc2  = uc * uc;
        const double vc2  = vc * vc;
        const double fx2  = fx * fx;
        const double fy2  = fy * fy;
        const double ifx  = 1.0 / fx;
        const double ify  = 1.0 / fy;

        Mat26 J;
        J << -fx * idepth, 0, uc * idepth, ucvc * ify, -(fx2 + uc2) * ifx,
            fx * ify * vc, 0, -fy * idepth, vc * idepth, (fy2 + vc2) * ify,
            -ucvc * ifx, -fy * ifx * uc;
        return J;
    }

};  // class PixelFlow

}  // namespace dso

#endif  // DSO_PIXEL_FLOW_H_