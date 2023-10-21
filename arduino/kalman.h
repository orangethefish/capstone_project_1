#ifndef KALMAN_ROLL_PITCH_H
#define KALMAN_ROLL_PITCH_H

#include <math.h>

#define g 9.80665f


typedef struct{
    float phi_rad;
    float theta_rad;

    float P[4];
    float Q[2];
    float R[3];
}KalmanRollPitch;

void KalmanRollPitch_Init(KalmanRollPitch *kal, float Pinit, float *Q, float *R);
void KalmanRollPitch_Predict(KalmanRollPitch *kal, float *gyr_rps, float T);
void KalmanRollPitch_Update(KalmanRollPitch *kal, float *acc_mps2);

#endif