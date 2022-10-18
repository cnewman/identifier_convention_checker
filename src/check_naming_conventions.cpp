#include <check_naming_conventions.hpp>
#include <string>
#include <iterator>
#include <iostream>
int main(int argc, char** argv){
        CheckNamingConventionsPolicy* cat = new CheckNamingConventionsPolicy();
        std::istreambuf_iterator<char> begin{std::cin}, end;
        std::string srcML_string(begin, end);
        srcSAXController control(srcML_string);
        srcSAXEventDispatch::srcSAXEventDispatcher<> handler({cat}, false);
        control.parse(&handler); //Start parsing	
	return 0;
}