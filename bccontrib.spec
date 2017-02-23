Summary:	Some cryptographic functions, in Java compatible to BouncyCastle
Name:		bccontrib
Version:	1.0
Release:	1
License:	MIT and GPLv2+
Group:		Development/Java
URL:		https://github.com/jitsi/%{name}/
Source0:	https://github.com/jitsi/%{name}/archive/%{name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.bouncycastle:bcprov-jdk15on)

Requires:	java-headless
Requires:	javapackages-tools
Requires:	bouncycastle

%description
This project contains the Skein hash function, the Threefish encryption
function and the Fortuna random generator as a Java implementation. The API
is designed to be compatible to BouncyCastle.

%files -f .mfiles
%doc README
%doc LICENSE

#----------------------------------------------------------------------------

%package	javadoc
Summary:	Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{name}-%{version}
# Delete prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Fix missing version
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-surefire-plugin']]" "
	<version>any</version>"
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-bundle-plugin']]" "
	<version>any</version>"
 
# Add the META-INF/INDEX.LIST (fix jar-not-indexed warning) and
# the META-INF/MANIFEST.MF to the jar archive
%pom_add_plugin :maven-jar-plugin . "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

# Fix JAR name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

