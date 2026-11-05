# Exact conditional zero-flux identity for the finite one-species model

**Date:** 2026-11-05. **Status:** analytic finite-model proof with executable
regression checks. This note is not a Lean theorem or an identification with
Bernhard Mueller's unavailable source-pinned theorem.

The corrected [`F01-axis3-v2` sampler](../scripts/oph_n2_flux_mc.py) has an exact
one-species negative control: the conditional expectation of each oriented
plaquette's sine flux is zero. Its separated slice correlator is also zero in
the declared equilibrium measure. Individual sampled fluxes need not vanish.

## Model and hypotheses

Let the finite periodic lattice be \(\Lambda=(\mathbb Z/L\mathbb Z)^4\), with
integer \(L\ge4\). The sampler uses even \(L\) for its red/black updates; the
identity itself needs no evenness. At each site there is one complex scalar
\(\psi_x\). For every positively oriented nearest-neighbor edge
\(e=(x,x+e_\mu)\), there is one \(U_e=e^{i\theta_e}\in U(1)\) and one
conductance \(w_e>0\). The joint density, with respect to complex Lebesgue
measure, independent Haar link measures, and \(dw_e\), is proportional to

\[
\left(\prod_e w_e^{\alpha-1}e^{-\beta w_e}\right)
\exp\left[-m^2\sum_x|\psi_x|^2
-\sum_{e=(x,y)}w_e|\psi_x-U_e\psi_y|^2\right],
\qquad m^2,\alpha,\beta>0.
\]

The positive anchor and Gamma rates give a finite normalizing integral:
drop the nonnegative link mismatch term to bound it by a product of finite
Gaussian and Gamma integrals. There is **no plaquette action or other term
coupling link variables**. Given \((\psi,w)\), all positively oriented link
variables are independent. Oppositely traversing a stored link means taking its
complex conjugate; it is not an additional independent variable.

This is the precise model implemented by the fork's independent sampler. The
proof requires its specified measure and observable. It does not assert that
the model is forced by OPH's axioms or realized in nature.

## Single-link conditional mean

For \(e=(x,y)\), write \(Q_e=\overline{\psi_x}\psi_y\). Expanding the mismatch
gives

\[
|\psi_x-U_e\psi_y|^2
=|\psi_x|^2+|\psi_y|^2-2\operatorname{Re}(U_eQ_e).
\]

For \(Q_e\ne0\), set \(\kappa_e=2w_e|Q_e|\) and
\(\gamma_e=\arg Q_e\). The conditional density of \(\theta_e\) is proportional
to \(\exp[\kappa_e\cos(\theta_e+\gamma_e)]\). Define the real integrals

\[
I_0(\kappa)=\frac1{2\pi}\int_{-\pi}^{\pi}e^{\kappa\cos u}\,du,
\qquad
I_1(\kappa)=\frac1{2\pi}\int_{-\pi}^{\pi}\cos u\,e^{\kappa\cos u}\,du.
\]

The imaginary part of the shifted integral vanishes by oddness. Therefore

\[
M_e:=\mathbb E[U_e\mid\psi,w]
=r_e e^{-i\gamma_e},\qquad
r_e=I_1(\kappa_e)/I_0(\kappa_e)\in\mathbb R.
\]

For \(\kappa\ge0\), pairing positive and negative cosine contributions in
\(I_1\) gives \(r_e\ge0\); also \(r_e<1\) for finite \(\kappa_e\) because the
conditional distribution has positive density on the whole circle. These
bounds are not needed for the zero imaginary part, but show that the resulting
mean Wilson product is nonnegative.

If \(Q_e=0\), the conditional link is uniform, so \(M_e=0\). Equivalently
\(I_1(0)=0\). No choice of \(\arg0\) is needed in the proof; the code multiplies
its arbitrary zero-angle convention by the exactly zero radial factor.

## Plaquette identity

For a site with nonzero field define \(s_x=\psi_x/|\psi_x|\in U(1)\). If both
endpoints of an edge are nonzero, then

\[
e^{-i\arg(\overline{\psi_x}\psi_y)}=s_x\overline{s_y},
\qquad M_{xy}=r_{xy}s_x\overline{s_y}.
\]

The correctly oriented \((0,1)\) plaquette is

\[
P_x=U_0(x)U_1(x+e_0)
\overline{U_0(x+e_1)}\,\overline{U_1(x)}.
\]

For \(L\ge4\), these are four distinct stored links. Conditional independence
therefore gives

\[
\mathbb E[P_x\mid\psi,w]
=M_0(x)M_1(x+e_0)
\overline{M_0(x+e_1)}\,\overline{M_1(x)}.
\]

If a corner field is zero, an adjacent \(Q_e\) vanishes, and the product is
zero. Otherwise all site phases cancel around the loop, leaving

\[
\mathbb E[P_x\mid\psi,w]
=r_0(x)r_1(x+e_0)r_0(x+e_1)r_1(x)\in\mathbb R_{\ge0}.
\]

As a consequence, for every fixed finite \((\psi,w)\),

\[
\boxed{\mathbb E[\operatorname{Im}P_x\mid\psi,w]=0.}
\]

This is a conditional expectation identity, not an assertion that \(P_x=1\)
or that sampled \(\operatorname{Im}P_x\) is zero. For example at \(L=4\),
choose \(U_1(x)=e^{i\pi x_0/2}\) and \(U_0=U_2=U_3=1\). Then \(P_x=i\)
everywhere, including the periodic boundary, and every sine flux equals one.
The conditional density has support near this configuration.

## Separated slices and the contact exception

Use coordinate axis 3 as the declared transfer direction, and define

\[
F_t=L^{-3}\sum_{x_0,x_1,x_2}\operatorname{Im}P_{(x_0,x_1,x_2,t)}.
\]

Linearity gives \(\mathbb E[F_t\mid\psi,w]=0\). The links used in \(F_t\)
all have directions 0 or 1 and base-site coordinate \(x_3=t\). For distinct
\(t,s\pmod L\), these link sets are disjoint. The slices are conditionally
independent given \((\psi,w)\), even though their field and conductance inputs
may be statistically dependent in the joint measure. Thus

\[
\boxed{\mathbb E[F_tF_s\mid\psi,w]
=\mathbb E[F_t\mid\psi,w]\mathbb E[F_s\mid\psi,w]=0,
\qquad t\ne s\pmod L.}
\]

Taking expectations yields \(\mathbb E[F_t]=0\) and the equilibrium connected
correlator \(\mathbb E[F_tF_s]-\mathbb E[F_t]\mathbb E[F_s]=0\) at separated
slices. All observables are bounded, so these conditional-expectation steps
require no extra integrability assumption. A finite Monte Carlo estimate can
fluctuate away from zero; subtracting its estimated mean squared also introduces
finite-sample bias. No equilibration or error-bar certificate follows from this
identity.

At contact, \(F_t\) and itself share links:
\(\mathbb E[F_t^2\mid\psi,w]\) is generally positive, while
\(\mathbb E[F_t\mid\psi,w]^2=0\). Consequently the product of conditional
slice means is valid for this separated correlator and invalid for its contact
variance. The sampler now withholds the Rao–Blackwell contact entry.

## Closed finite obligation and remaining boundary

This closes the conditional one-species zero-sine-flux calculation for the
explicit finite model, including the chosen separated-slice observable. It
does not establish a physical photon, a no-pole result in every observable,
absence of fluctuating flux, or the intended source theorem in another model.
With two or more scalar species,
\(Q_{xy}=\sum_a\overline{\psi_{x,a}}\psi_{y,a}\) need not have a telescoping
single-site phase. A plaquette action also destroys the independent-link
conditional factorization. Both changes require separate arguments.

The checks in [test_n1_conditional_flux.py](../tests/test_n1_conditional_flux.py)
compare the link mean with direct quadrature of the original link Boltzmann
factor, include zero-field corners, verify disjoint slice-link sets, exercise
the actual N=1 sampler, exhibit nonzero raw flux, and demonstrate failure of the
one-species phase conclusion for a two-species fixture.

```sh
python -m unittest discover -s tests -p test_n1_conditional_flux.py -v
```
