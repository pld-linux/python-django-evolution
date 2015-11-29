#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	django-evolution
Summary:	Schema evolution for Django
Name:		python-django-evolution
Version:	0.6.8
Release:	2
License:	BSD
Group:		Development/Languages
URL:		http://code.google.com/p/django-evolution/
Source0:	http://pypi.python.org/packages/source/d/django_evolution/django_evolution-%{version}.tar.gz
# Source0-md5:	e3393e745810ecffc7bbe647effcf86a
BuildRequires:	python-coverage
BuildRequires:	python-devel
BuildRequires:	python-django >= 1.1.1
BuildRequires:	python-nose
BuildRequires:	python-pyflakes
BuildRequires:	python-setuptools
BuildRequires:	python-sqlite
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	sed >= 4.0
Requires:	python-django >= 1.1.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
When you run ./manage.py syncdb, Django will look for any new models
that have been defined, and add a database table to represent those
new models. However, if you make a change to an existing model,
./manage.py syncdb will not make any changes to the database.

This is where Django Evolution fits in. Django Evolution is an
extension to Django that allows you to track changes in your models
over time, and to update the database to reflect those changes.

%prep
%setup -q -n django_evolution-%{version}
%{__sed} -i -e 's/^from ez_setup/#from ez_setup/' setup.py
%{__sed} -i -e 's/^use_setuptools()/#use_setuptools()/' setup.py

%{__rm} -r *.egg-info

%build
%py_build

%if %{with tests}
%{__python} tests/runtests.py
%{__python} tests/run-pyflakes.py
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install \
	--root $RPM_BUILD_ROOT

%py_postclean

# Delete tests. They aren't useful in an installed system
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/django_evolution/tests
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README docs
%{py_sitescriptdir}/django_evolution
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/django_evolution-%{version}-*.egg-info
%endif
