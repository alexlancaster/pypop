<?xml version='1.0'?>

<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version='1.0'>

 <xsl:param name="use.natbib.citation.in.role" select="1"/>

<!-- from the Natbib list of commands, for implementation reference only

This XSL file only implements the non-starred version (*) of the commands listed 
in the first group below:

\citet{key} ==>>                Jones et al. (1990)
\citet*{key} ==>>               Jones, Baker, and Smith (1990)
\citep{key} ==>>                (Jones et al., 1990)
\citep*{key} ==>>               (Jones, Baker, and Smith, 1990)
\citep[chap. 2]{key} ==>>       (Jones et al., 1990, chap. 2)
\citep[e.g.][]{key} ==>>        (e.g. Jones et al., 1990)
\citep[e.g.][p. 32]{key} ==>>   (e.g. Jones et al., p. 32)
\citeauthor{key} ==>>           Jones et al.
\citeauthor*{key} ==>>          Jones, Baker, and Smith
\citeyear{key} ==>>             1990


Then, \citet{key}  ==>>  Jones et al. (1990)    ||   Jones et al. [21]
\citep{key}  ==>> (Jones et al., 1990)    ||   [21]
\citep{key1,key2}  ==>> (Jones et al., 1990; Smith, 1989) || [21,24]
or  (Jones et al., 1990, 1991)  || [21,24]
or  (Jones et al., 1990a,b)     || [21,24]

\cite{key} is the equivalent of \citet{key} in author-year mode
and  of \citep{key} in numerical mode

Full author lists may be forced with \citet* or \citep*, e.g.
\citep*{key}      ==>> (Jones, Baker, and Williams, 1990)
Optional notes as:
\citep[chap. 2]{key}    ==>> (Jones et al., 1990, chap. 2)
\citep[e.g.,][]{key}    ==>> (e.g., Jones et al., 1990)
\citep[see][pg. 34]{key}==>> (see Jones et al., 1990, pg. 34)
(Note: in standard LaTeX, only one note is allowed, after the ref.
Here, one note is like the standard, two make pre- and post-notes.)

\citealt{key}          ==>> Jones et al. 1990
\citealt*{key}         ==>> Jones, Baker, and Williams 1990
\citealp{key}          ==>> Jones et al., 1990
\citealp*{key}         ==>> Jones, Baker, and Williams, 1990

Additional citation possibilities (both author-year and numerical modes)
\citeauthor{key}       ==>> Jones et al.
\citeauthor*{key}      ==>> Jones, Baker, and Williams
\citeyear{key}         ==>> 1990
\citeyearpar{key}      ==>> (1990)
\citetext{priv. comm.} ==>> (priv. comm.)

-->


 <xsl:template match="biblioentry|bibliomixed" mode="citation-to-prefix">
  <xsl:if test="$use.natbib.citation.in.role != 1">
   <xsl:text>[</xsl:text>
  </xsl:if>
 </xsl:template>
 
 <xsl:template match="biblioentry|bibliomixed" mode="citation-to-suffix">
  <xsl:if test="$use.natbib.citation.in.role != 1">
   <xsl:text>]</xsl:text>
  </xsl:if>
 </xsl:template>

 <xsl:template match="citation" name="citation">
  <xsl:variable name="targets" select="key('id',.)"/>
  <xsl:variable name="target" select="$targets[1]"/>
  <xsl:variable name="refelem" select="local-name($target)"/>

  <xsl:call-template name="check.id.unique">
    <xsl:with-param name="linkend" select="@linkend"/>
  </xsl:call-template>

  <xsl:call-template name="anchor"/>

  <xsl:choose>
    <xsl:when test="count($target) = 0">
      <xsl:message>
	<xsl:text>Citation to nonexistent id: </xsl:text>
	<xsl:value-of select="."/>
      </xsl:message>
      <xsl:text>???</xsl:text>
    </xsl:when>

    <xsl:when test="$target/@xreflabel">
      <a>
        <xsl:attribute name="href">
          <xsl:call-template name="href.target">
            <xsl:with-param name="object" select="$target"/>
          </xsl:call-template>
        </xsl:attribute>
        <xsl:call-template name="xref.xreflabel">
          <xsl:with-param name="target" select="$target"/>
        </xsl:call-template>
      </a>
    </xsl:when>

   <xsl:otherwise>
    <xsl:variable name="href">
     <xsl:call-template name="href.target">
      <xsl:with-param name="object" select="$target"/>
     </xsl:call-template>
    </xsl:variable>
    
    <xsl:apply-templates select="$target" mode="citation-to-prefix"/>
    
    <a href="{$href}">
     <xsl:if test="$target/title or $target/*/title">
      <xsl:attribute name="title">
       <xsl:apply-templates select="$target" mode="citation-title"/>
      </xsl:attribute>
     </xsl:if>
     <xsl:apply-templates select="$target" mode="citation-to">
      <xsl:with-param name="referrer" select="."/>
      <xsl:with-param name="xrefstyle" select="@role"/>
     </xsl:apply-templates>
    </a>
    
    <xsl:apply-templates select="$target" mode="citation-to-suffix"/>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <xsl:template name="natbib-text">
  <xsl:param name="entry"/>
  <xsl:param name="citationrole" select="'citep'"/>

  <xsl:variable name="authors" select="$entry//author"/>
  <xsl:variable name="year" select="$entry//pubdate[1]"/>
  <xsl:variable name="title" select="$entry//citetitle[1]|$entry//title[1]"/>

  <xsl:variable name="extra-text1">
   <xsl:choose>
    <xsl:when test="contains($citationrole, '[')">1</xsl:when>
    <xsl:otherwise>0</xsl:otherwise>
   </xsl:choose>
  </xsl:variable>

  <xsl:variable name="citationstyle">
   <xsl:choose>
    <xsl:when test="$extra-text1 = 1">
     <xsl:value-of select="substring-before($citationrole, '[')"/>
    </xsl:when>
    <xsl:otherwise><xsl:value-of select="$citationrole"/></xsl:otherwise>
   </xsl:choose>
  </xsl:variable>

  <xsl:variable name="rest1">
   <xsl:if test="$citationstyle='citep'">
    <xsl:if test="$extra-text1 = 1">
     <xsl:value-of select="substring-after($citationrole, '[')"/>
    </xsl:if>
   </xsl:if>
  </xsl:variable>

  <xsl:variable name="extra-text2">
   <xsl:choose>
     <xsl:when test="contains($rest1, '[')">1</xsl:when>
    <xsl:otherwise>0</xsl:otherwise>
   </xsl:choose>
  </xsl:variable>

  <xsl:variable name="rest2">
   <xsl:if test="$extra-text2 = 1">
    <xsl:value-of select="substring-after($rest1, '[')"/>
   </xsl:if>
  </xsl:variable>

  <xsl:variable name="first">
   <xsl:value-of select="substring-before($rest1, ']')"/>
  </xsl:variable>

  <xsl:variable name="second">
   <xsl:value-of select="substring-before($rest2, ']')"/>
  </xsl:variable>

  <xsl:variable name="authortext">
   <xsl:choose>

    <!-- if no authors, just use the id -->
    <xsl:when test="count($authors) = 0">
     <xsl:value-of select="$entry/@id"/>
    </xsl:when>
    
    <xsl:when test="count($authors) = 1">
     <xsl:value-of select="$authors/surname"/>
    </xsl:when>
    
    <xsl:when test="count($authors) = 2">
     <xsl:value-of select="$authors[1]/surname"/>
     <xsl:text> &amp; </xsl:text>
     <xsl:value-of select="$authors[2]/surname"/>
    </xsl:when>
    
    <xsl:otherwise>
     <xsl:value-of select="$authors[1]/surname"/>
     <xsl:text> et al.</xsl:text>
    </xsl:otherwise>
   </xsl:choose>
  </xsl:variable>

  <xsl:choose>

   <xsl:when test="$citationstyle='citep' or $citationstyle=''">
    <xsl:text> (</xsl:text>

    <xsl:choose>
     <xsl:when test="$extra-text1=1">
      <xsl:if test="$extra-text1=1 and $extra-text2=1">
       <xsl:value-of select="$first"/>
       <xsl:text> </xsl:text>
      </xsl:if>
      <xsl:value-of select="$authortext"/>
      <xsl:if test="$year!='' and not($extra-text2=1 and $second!='')">
       <xsl:text>, </xsl:text>
       <xsl:value-of select="$year"/>
      </xsl:if>
      <xsl:if test="$extra-text1=1 and $extra-text2=0 and $first!=''">
       <xsl:text>, </xsl:text>
       <xsl:value-of select="$first"/>
      </xsl:if>
      <xsl:if test="$extra-text1=1 and $extra-text2=1 and $second!=''">
       <xsl:text>, </xsl:text>
       <xsl:value-of select="$second"/>
      </xsl:if>
     </xsl:when>
     <xsl:otherwise>
      <xsl:value-of select="$authortext"/>
      <xsl:if test="$year!=''">
       <xsl:text>, </xsl:text>
       <xsl:value-of select="$year"/>
      </xsl:if>
     </xsl:otherwise>
    </xsl:choose>
    <xsl:text>)</xsl:text>
   </xsl:when>

   <xsl:when test="$citationstyle='citet'">
    <xsl:value-of select="$authortext"/>
    <xsl:text> (</xsl:text>
    <xsl:value-of select="$year"/>
    <xsl:text>)</xsl:text>
   </xsl:when> 

   <xsl:when test="$citationstyle='citeauthor'">
    <xsl:value-of select="$authortext"/>
   </xsl:when> 

   <xsl:when test="$citationstyle='citeyear'">
    <xsl:value-of select="$year"/>
   </xsl:when> 
   
   <xsl:when test="$citationstyle='citeyearpar'">
    <xsl:text>(</xsl:text>
    <xsl:value-of select="$year"/>
    <xsl:text>)</xsl:text>
   </xsl:when> 

   <xsl:otherwise>
    <xsl:message>Unrecognized citationstyle: <xsl:value-of
    select="$citationstyle"/>
    </xsl:message>
   </xsl:otherwise>

  </xsl:choose>


 </xsl:template>

 <xsl:template match="biblioentry|bibliomixed" mode="citation-to">
  <xsl:param name="referrer"/>
  <xsl:param name="xrefstyle"/>

  <!-- handles both biblioentry and bibliomixed -->
  <xsl:choose>

   <xsl:when test="string(.) = ''">
    <xsl:variable name="bib" select="document($bibliography.collection)"/>
    <xsl:variable name="id" select="@id"/>
    <xsl:variable name="entry" select="$bib/bibliography/*[@id=$id][1]"/>
    <xsl:choose>
     <xsl:when test="$entry">
      
      <xsl:choose>
       <xsl:when test="$use.natbib.citation.in.role != 1">
	
	<xsl:choose>
	 <xsl:when test="local-name($entry/*[1]) = 'abbrev'">
	  <xsl:apply-templates select="$entry/*[1]"/>
	 </xsl:when>
	 <xsl:otherwise>
	  <xsl:value-of select="@id"/>
	 </xsl:otherwise>
	</xsl:choose>

       </xsl:when>
       
       <xsl:otherwise>
	<xsl:call-template name="natbib-text">
	 <xsl:with-param name="entry" select="$entry"/>
	 <xsl:with-param name="citationrole" select="$xrefstyle"/>
	</xsl:call-template>
       </xsl:otherwise>

      </xsl:choose>

     </xsl:when>
     
     <xsl:otherwise>
      <xsl:message>
       <xsl:text>No bibliography entry: </xsl:text>
       <xsl:value-of select="$id"/>
       <xsl:text> found in </xsl:text>
       <xsl:value-of select="$bibliography.collection"/>
      </xsl:message>
      <xsl:value-of select="@id"/>
     </xsl:otherwise>
    </xsl:choose>
   </xsl:when>
   
   <xsl:otherwise>

    <xsl:choose>
     <xsl:when test="$use.natbib.citation.in.role != 1">
      
      <xsl:choose>
       <xsl:when test="local-name(*[1]) = 'abbrev'">
	<xsl:apply-templates select="*[1]"/>
       </xsl:when>
       <xsl:otherwise>
	<xsl:value-of select="@id"/>
       </xsl:otherwise>
      </xsl:choose>
      
     </xsl:when>

     <xsl:otherwise>
      <xsl:call-template name="natbib-text">
       <xsl:with-param name="entry" select="."/>
       <xsl:with-param name="citationrole" select="$xrefstyle"/>
      </xsl:call-template>

     </xsl:otherwise>

    </xsl:choose>
    
   </xsl:otherwise>

  </xsl:choose>
 </xsl:template>
 
<xsl:template match="biblioentry|bibliomixed" mode="citation-title">
  <!-- handles both biblioentry and bibliomixed -->
  <xsl:variable name="title">
    <xsl:text>[</xsl:text>
    <xsl:choose>
      <xsl:when test="local-name(*[1]) = 'abbrev'">
        <xsl:apply-templates select="*[1]"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="@id"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:text>]</xsl:text>
  </xsl:variable>

  <xsl:value-of select="$title"/>
</xsl:template>


</xsl:stylesheet>

