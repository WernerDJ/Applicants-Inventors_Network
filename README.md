# Applicants-Inventors_Network

The code has been designed to analize a patent list obtained from a patent search. In this case the search engine used was that of Orbit Intelligence \n
Other patent databases will provide a different output format or a different type of file (like a csv, xml, etc)
The result list is then analized to establish connections between the different applicants. The connections depend on the different applicants disclosing the same inventors.
That can be either because an application (or more) present both applicants as the result of a collaboration, because the inventors have changed employers durig their careers or because a company has aquired another which already had patents filed and with the compeny their R&D crew. 
This code take an excel file as input where there are two columns. In one column with header name "Applicants" if an application presents more than one applicant they are separated by new lines (\n), the other colummn presents the inventors, also separated by new lines.
At the beginnig of the code there is a list named Tochange, this list is of applicants easily recognizable by one word. Applicants often appear with different wordings like in one patent as something Pharma and in another Pharmaceuticals, or Electrical Engineering here and Electronics there. This might give a network with several applicants heavily interconnected that are really just one company. Using just the single word that is the common denominator, when that name is easily recognizable enables the ellaboration of a proper network.
